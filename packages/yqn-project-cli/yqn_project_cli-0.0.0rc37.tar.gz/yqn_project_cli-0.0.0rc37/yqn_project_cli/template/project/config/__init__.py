# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/24
import os
from yqn_project_cli.utils import conf_loader


class ProjectConfig:
    id = "${app_id}"
    name = "${project_name}"

    version = '1.0.0'
    version_int = 1 * 10000 + 0 * 100 + 0 * 1

    heartbeat_url = '/heartbeat/'
    project_base_dir = os.path.dirname(os.path.dirname(__file__))
    project_father_dir = os.path.dirname(project_base_dir)

    resources = os.path.join(project_base_dir, 'resources')  # resource_path
    outputs = os.path.join(project_base_dir, 'outputs')  # output_path


class LoggerConfig:
    app_id = ProjectConfig.id
    app_name = ProjectConfig.name
    log_path = '/app/' + app_name + '/log/'
    try:
        os.makedirs(log_path, exist_ok=False)
    except Exception as e:
        pass


local_conf_loader = conf_loader(os.path.join(ProjectConfig.project_father_dir, '.{}_config.py'.format(ProjectConfig.name)))


class ApolloClientConfig:
    apollo_meta_server_url = local_conf_loader('APOLLO_META_SERVER_URL', 'http://192.168.10.227:8080')
    apollo_cluster = local_conf_loader('APOLLO_CLUSTER', "qa")
    apollo_app_id = local_conf_loader('APOLLO_APP_ID', ProjectConfig.id)
    apollo_app_name = local_conf_loader('APOLLO_APP_NAME', ProjectConfig.name)
    apollo_env = local_conf_loader('APOLLO_ENV', "FAT")


class ODPSConfig:
    odps_access_id = local_conf_loader('ODPS_ACCESS_ID', '')
    odps_secret_access_key = local_conf_loader('ODPS_SECRET_ACCESS_KEY', '')
    odps_project = local_conf_loader('ODPS_PROJECT', '')
    odps_endpoint = local_conf_loader('ODPS_ENDPOINT', '')


class MySQLConfig:
    mysql_engine = local_conf_loader('MYSQL_ENGINE', '')
    mysql_username = local_conf_loader('MYSQL_USERNAME', '')
    mysql_password = local_conf_loader('MYSQL_PASSWORD', '')
    mysql_host = local_conf_loader('MYSQL_HOST', '')
    mysql_port = local_conf_loader('MYSQL_PORT', '')
    mysql_charset = local_conf_loader('MYSQL_CHARSET', '')
    mysql_database = local_conf_loader('MYSQL_DATABASE', '')


class ESConfig:
    es_host = local_conf_loader('ES_HOST', '')
    es_port = local_conf_loader('ES_PORT', '')
    es_username = local_conf_loader('ES_USERNAME', '')
    es_password = local_conf_loader('ES_PASSWORD', '')


class RedisConfig:
    redis_host = local_conf_loader('REDIS_HOST', '')
    redis_port = local_conf_loader('REDIS_PORT', '')
    redis_db = local_conf_loader('REDIS_DB', '')
    redis_password = local_conf_loader('REDIS_PASSWORD', '')
