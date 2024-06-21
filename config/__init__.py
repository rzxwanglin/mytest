# -*- coding: utf-8 -*-
# !/usr/bin/env python
# 配置读取
import configparser
import copy
import json,platform
import os
from rhino_v2_utilis.handler.util import get_private_ip, get_public_ip
from rhino_v2_utilis.config import ConfigHandler

# 获取当前工作目录
current_path = os.getcwd()

CONFIG_DIR =current_path+'\\config\\'
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.cfg")  # config.cfg文件路径
CONFIG_OBJ = configparser.ConfigParser()
CONFIG_OBJ.read(os.path.join(CONFIG_DIR, "config.cfg"), encoding="utf-8")

def attribute_str(Section, Option, default):
    try:
        return CONFIG_OBJ.get(Section, Option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default

def attribute_int(Section, Option, default):
    try:
        return int(CONFIG_OBJ.getint(Section, Option))
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        return default

def attribute_bool(Section, Option, default):
    try:
        return bool(CONFIG_OBJ.getboolean(Section, Option))
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
        return default

def attribute_json(Section, Option, default):
    try:
        return json.loads(CONFIG_OBJ.get(Section, Option))
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError, json.decoder.JSONDecodeError):
        return default

CRAWL_COMPONENTS_CONFIG = attribute_json("crawl_components", "config", {})
SITE_TYPE = attribute_str("SITE_TYPE", "SITE_TYPE", "google")
TASK_INTERFACE_TYPE = attribute_str("INTERFACE_SETTINGS", "TASK_INTERFACE_TYPE", "redis")
DATA_INTERFACE_TYPE = attribute_str("INTERFACE_SETTINGS", "DATA_INTERFACE_TYPE", "redis")
DATA_INTERFACE_SSL = attribute_bool("INTERFACE_SETTINGS", "DATA_INTERFACE_SSL", False)
TASK_INTERFACE_SSL = attribute_bool("INTERFACE_SETTINGS", "TASK_INTERFACE_SSL", False)


PROXY_ENABLE = attribute_bool("PROXY", "ENABLE", True)  # 代理开关

PROXY_LIST = []
if PROXY_ENABLE:
    PROXY_LIST = attribute_str("PROXY", "PROXY_LIST", "").split(",")



DATA_DB_CONFIG = attribute_json("REDIS-DATA", "CONFIG", {})
TASK_DB_CONFIG = attribute_json( "REDIS-TASK", "CONFIG", {})
TAG_LIST = attribute_json("GLOBAL-SETTINGS", "TAG_LIST", [])
CRAWL_COMPONENTS_CONFIG.update(**{
        "task_host": TASK_DB_CONFIG['ip'],
        "task_port": TASK_DB_CONFIG['port'],
        "task_password": TASK_DB_CONFIG['password'],
        "task_db": TASK_DB_CONFIG['db_name'],
        "data_host": DATA_DB_CONFIG['ip'],
        "data_port": DATA_DB_CONFIG['port'],
        "data_db": DATA_DB_CONFIG['db_name'],
        "data_password": DATA_DB_CONFIG['password'],
        "project_list": TAG_LIST,
    })


if DATA_INTERFACE_TYPE == "redis" and DATA_INTERFACE_SSL:
    CRAWL_COMPONENTS_CONFIG.update(**{
        "data_redis_ssl": DATA_INTERFACE_SSL,
    })

if TASK_INTERFACE_TYPE == "redis" and TASK_INTERFACE_SSL:
    CRAWL_COMPONENTS_CONFIG.update(**{
        "task_redis_ssl": TASK_INTERFACE_SSL,
    })

ConfigHandler.format(**CRAWL_COMPONENTS_CONFIG)
# 公网内网IP获取
PUBLIC_IP = get_public_ip()
PRIVATE_IP = get_private_ip()
