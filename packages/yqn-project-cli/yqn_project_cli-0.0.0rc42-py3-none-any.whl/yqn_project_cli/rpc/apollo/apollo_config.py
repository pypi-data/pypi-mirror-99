# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/1
import inspect
from yqn_project_cli.rpc.eureka import eureka_client
from yqn_project_cli.rpc.apollo.apollo_client import ApolloClient
from yqn_project_cli.rpc import RPCConfigBase
from yqn_project_cli.utils import host_ip


class ApolloConfig(RPCConfigBase):

    def __init__(self, **kwargs):
        super(ApolloConfig, self).__init__(**kwargs)

        self.apollo_app_id = self.client_config.apollo_app_id
        self.apollo_cluster = self.client_config.apollo_cluster
        self.apollo_meta_server_url = self.client_config.apollo_meta_server_url
        self.apollo_env = self.client_config.apollo_env

        self.conf_management = {}
        self.services = {}

    def init_apollo(self):
        apollo_client = ApolloClient(app_id=self.apollo_app_id,
                                     cluster=self.apollo_cluster,
                                     config_server_url=self.apollo_meta_server_url,
                                     env=self.apollo_env)

        apollo_client.start(lambda: self.reload(apollo_client))
        # apollo_client.start(lambda: self.manage_servers(apollo_client))  # hot update

        self.connector = apollo_client

    def init_eureka(self):
        eureka_client.init(eureka_server=self.connector.get_value('eureka_url'),
                           app_name=self.project_config.name,
                           instance_ip=host_ip(),
                           instance_port=int(self.project_config.id),
                           status_page_url=self.project_config.heartbeat_url,
                           health_check_url=self.project_config.heartbeat_url)

    def manage_servers(self, apollo_client):
        self.conf_management = apollo_client._cache['application']
        for name, elder_server in self.services.items():
            if elder_server is self or not callable(getattr(elder_server, 'reconnect', False)):
                continue

            # server reconnect depend on certain conf_management attrs
            elder_server.reconnect(**self.conf_management)

    def reload(self, apollo_client):

        # va
        # if 'certain_self_settings_namespace' in apollo_client._cache:
        #     self.conf_management = apollo_client._cache['certain_self_settings_namespace']
        #
        # else:
        #     self.conf_management = apollo_client._cache['application']

        # vb
        self.conf_management = apollo_client._cache['application']

        # vc
        # for key, value in inspect.getmembers(ApolloConfigMapping):
        #     if not key.startswith('__') and not callable(value):
        #         self.conf_management[key] = apollo_client.get_value(key)

        # vd
        # self.conf_management = dict(
        #
        #     eureka_url=apollo_client.get_value('eureka_url'),
        #
        #     es_host=apollo_client.get_value('es_host'),
        #     es_port=apollo_client.get_value('es_port'),
        #     es_username=apollo_client.get_value('es_username'),
        #     es_password=apollo_client.get_value('es_password'),
        #
        #     mysql_engine=apollo_client.get_value('mysql_engine'),
        #     mysql_username=apollo_client.get_value('mysql_username'),
        #     mysql_password=apollo_client.get_value('mysql_password'),
        #     mysql_host=apollo_client.get_value('mysql_host'),
        #     mysql_port=apollo_client.get_value('mysql_port'),
        #     mysql_charset=apollo_client.get_value('mysql_charset'),
        #     mysql_database=apollo_client.get_value('mysql_database'),
        #     mysql_url=apollo_client.get_value('mysql_url'),
        #
        #     odps_access_id=apollo_client.get_value('odps_access_id'),
        #     odps_secret_access_key=apollo_client.get_value('odps_secret_access_key'),
        #     odps_project=apollo_client.get_value('odps_project'),
        #     odps_endpoint=apollo_client.get_value('odps_endpoint'),
        #
        # )

    def connect(self, **kwargs):
        self.init_apollo()
        self.init_eureka()
        return self.conf_management

    def close(self, **kwargs):
        pass

    def reconnect(self, **kwargs):
        pass
