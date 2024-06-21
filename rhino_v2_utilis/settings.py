# -*-coding:utf-8 -*-
"""
# File       : settings.py
# Time       ：2023/6/21 10:06
# Author     ：caomengqi
# version    ：python 3.6
"""
from .config import ConfigHandler
from .handler.rhino_v2_platform_api import RhinoV2Api
from .handler.util import get_hostname

# 初始化redis任务配置 redis_task
TASK_REDIS_HOST = ConfigHandler.__get_property__(
    "task_host", RhinoV2Api.m_task_interface_params["ip"]
)
TASK_REDIS_PORT = ConfigHandler.__get_property__(
    "task_port", int(RhinoV2Api.m_task_interface_params["port"])
)
TASK_REDIS_DB = ConfigHandler.__get_property__(
    "task_db", int(RhinoV2Api.m_task_interface_params["db_name"])
)
TASK_REDIS_PASSWORD = ConfigHandler.__get_property__(
    "task_password", RhinoV2Api.m_task_interface_params["password"] or None
)

TASK_REDIS_CONFIG = {
    "host": TASK_REDIS_HOST,
    "port": TASK_REDIS_PORT,
    "password": TASK_REDIS_PASSWORD,
    "db": TASK_REDIS_DB,
    "max_connections": 64,
    "redis_ssl": ConfigHandler.__get_property__("task_redis_ssl", False) if ConfigHandler.__get_property__("task_redis_ssl", False) else ConfigHandler.__get_property__("redis_ssl", False),
    "kafka_ssl": ConfigHandler.__get_property__("task_kafka_ssl", False) if ConfigHandler.__get_property__("task_kafka_ssl", False) else ConfigHandler.__get_property__("kafka_ssl", False),
}
DATA_REDIS_CONFIG = {
    "host": ConfigHandler.__get_property__(
        "data_host", RhinoV2Api.m_data_interface_params.get("ip")
    ),
    "port": ConfigHandler.__get_property__(
        "data_port", int(RhinoV2Api.m_data_interface_params.get("port"))
    ),
    "password": ConfigHandler.__get_property__(
        "data_password", RhinoV2Api.m_data_interface_params.get("password") or None
    ),
    "db": ConfigHandler.__get_property__(
        "data_db", int(RhinoV2Api.m_data_interface_params.get("db_name"))
    ),
    "max_connections": 64,
    "redis_ssl": ConfigHandler.__get_property__("data_redis_ssl", False) if ConfigHandler.__get_property__(
        "data_redis_ssl", False) else ConfigHandler.__get_property__("redis_ssl", False),
    "kafka_ssl": ConfigHandler.__get_property__("data_kafka_ssl", False) if ConfigHandler.__get_property__(
        "data_kafka_ssl", False) else ConfigHandler.__get_property__("kafka_ssl", False),

}

DUPEFILTER_REDIS_CONDIF = {
    "host": TASK_REDIS_HOST,
    "port": TASK_REDIS_PORT,
    "password": TASK_REDIS_PASSWORD,
    "db": 2,
    "max_connections": 10,
    "capacity": 10000 * 10000,
    "rate": 0.0001 * 0.0001,
    "expire_day": 3 * 24 * 60 * 60,
    "redis_ssl": ConfigHandler.__get_property__("redis_ssl", False),
}
HOSTNAME = ConfigHandler.__get_property__("hostname", get_hostname())
USE_DUPEFILTER_KEY = (
    "{tag}:+"
    + ConfigHandler.__get_property__("site_type", "telegram")
    + ":{task}:dupefilter"
)

SITE_TYPE = ConfigHandler.__get_property__("site_type", "telegram")

PROJECT_LIST = ConfigHandler.__get_property__("project_list", RhinoV2Api.m_project_list)
DUPEFILTER_IS_OPEN = ConfigHandler.__get_property__("dupefilter", False)
