# Copyright 2021 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from cached_property import cached_property
from ebi_eva_common_pyutils.logger import AppLogger
from ebi_eva_common_pyutils.command_utils import run_command_with_output
from pymongo import MongoClient, uri_parser


class MongoDatabase(AppLogger):
    def __init__(self, uri: str, secrets_file: str = None, db_name: str = "admin", password_required: bool = True):
        self.uri = uri
        self.secrets_file = secrets_file
        self.db_name = db_name
        self.password_required = password_required

    @cached_property
    def uri_with_db_name(self):
        """
        Return URI with the database name substituted
        ex:
        If the URI is mongodb://user@localhost:27017/admin and database name is eva_fcatus_90,
        then the URI with the database name will be mongodb://user@localhost:27017/eva_fcatus_90?authSource=admin
        """
        if self.db_name == "admin":
            return self.db_name
        uri_components = uri_parser.parse_uri(self.uri)
        username_component = f"{uri_components['username']}@" if uri_components['username'] else ""
        # Hack needed to log in to a different DB but retain authentication source
        # See https://docs.mongodb.com/v4.0/reference/connection-string/#records-database and https://docs.mongodb.com/v4.0/reference/connection-string/#urioption.authSource
        uri_with_db_name = f"mongodb://{username_component}" + \
                           ",".join([node + ':' + str(port) for node, port in uri_components['nodelist']]) + \
                           f"/{self.db_name}"
        uri_with_db_name += f"?authSource=" \
                            f"{uri_components['options'].get('authSource', 'admin')}" if self.password_required else ""
        return uri_with_db_name

    @cached_property
    def mongo_handle(self):
        if self.secrets_file:
            with open(self.secrets_file) as secrets_file_handle:
                mongo_password = secrets_file_handle.read().strip()
            return MongoClient(self.uri, password=mongo_password)
        else:
            return MongoClient(self.uri)

    def __del__(self):
        self.mongo_handle.close()

    def _get_optional_secrets_file_stdin(self):
        if self.password_required and self.secrets_file:
            return f" < {self.secrets_file}"
        return ""

    def drop(self):
        self.mongo_handle.drop_database(self.db_name)

    def get_collection_names(self):
        return self.mongo_handle[self.db_name].list_collection_names()

    def get_indexes(self):
        collection_index_map = {}
        for collection_name in self.get_collection_names():
            collection_index_map[collection_name] = self.mongo_handle[self.db_name][collection_name].index_information()
        return collection_index_map

    def create_index_on_collections(self, collection_index_map):
        collection_index_map_copy = copy.deepcopy(collection_index_map)
        for collection_name, index_info_map in collection_index_map_copy.items():
            # Copy indexes from one collection to another See https://stackoverflow.com/a/51445278
            for name, index_info in index_info_map.items():
                keys = index_info['key']
                del (index_info['ns'])
                del (index_info['v'])
                del (index_info['key'])
                if 'background' in index_info:
                    del (index_info['background'])
                self.mongo_handle[self.db_name][collection_name].create_index(keys, name=name, **index_info)

    def enable_sharding(self):
        self.mongo_handle.admin.command({"enableSharding": self.db_name})

    def shard_collections(self, collections_shard_key_map, collections_to_shard):
        for collection_name in collections_to_shard:
            shard_key, shard_key_uniqueness_flag = collections_shard_key_map.get(collection_name, (["_id"], False))
            # Shard key representation in the format {"key1": 1, "key2": 1}
            shard_key_repr = "{{{0}}}".format(",".join([f'"{attribute}": 1' for attribute in shard_key]))
            shard_collection_command = f'sh.shardCollection(' \
                                       f'"{self.db_name}.{collection_name}", ' \
                                       f'{shard_key_repr}, {str(shard_key_uniqueness_flag).lower()})'
            sharding_command = f"mongo --host {self.uri}  " \
                               f"--eval " \
                               f"'{shard_collection_command}' "
            sharding_command += self._get_optional_secrets_file_stdin()
            run_command_with_output(f"Sharding collection {collection_name} in the database {self.uri_with_db_name} "
                                    f"with key {shard_key_repr}...", sharding_command,
                                    log_error_stream_to_output=True,)

    def dump_data(self, dump_dir):
        if self.password_required and not self.secrets_file:
            raise Exception("Cannot run mongodump without secrets file! See https://jira.mongodb.org/browse/TOOLS-1020")
        mongodump_command = f"mongodump --uri {self.uri_with_db_name}  --out {dump_dir}" + \
                            self._get_optional_secrets_file_stdin()
        run_command_with_output("mongodump", mongodump_command, log_error_stream_to_output=True)

    def restore_data(self, dump_dir, mongorestore_args=None):
        if self.password_required and not self.secrets_file:
            raise Exception("Cannot run mongorestore without secrets file! "
                            "See https://jira.mongodb.org/browse/TOOLS-1020")
        mongorestore_args = " ".join([f"--{arg} {val}"
                                      for arg, val in mongorestore_args.items()]) if mongorestore_args else ""
        mongorestore_command = f"mongorestore --uri {self.uri_with_db_name} " \
                               f"{mongorestore_args} " \
                               f"--dir {dump_dir} "
        mongorestore_command += self._get_optional_secrets_file_stdin()
        run_command_with_output("mongorestore", mongorestore_command, log_error_stream_to_output=True)
