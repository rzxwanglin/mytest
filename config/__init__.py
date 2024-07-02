# -*- coding: utf-8 -*-
# !/usr/bin/env python
# 配置读取
import configparser
import copy
import json,platform
import os
from rhino_v2_utilis.handler.util import get_private_ip, get_public_ip
from rhino_v2_utilis.config import ConfigHandler
from loguru import logger
from rhino_v2_utilis.handler.redis_handler import CRedisHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# 获取当前工作目录
current_path = os.getcwd()

CONFIG_DIR =current_path+'/config/'
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.cfg")  # config.cfg文件路径
logger.info(f'初始化配置路径：{CONFIG_PATH}')
CONFIG_OBJ = configparser.ConfigParser()
CONFIG_OBJ.read(CONFIG_PATH, encoding="utf-8")

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


log_path = attribute_str("SITE_TYPE", "log_path", "")



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





# 账号配置
platform_token_account_hash = attribute_str("account", "platform_token_account_hash", "")
fail_token_account_hash = attribute_str("account", "fail_token_account_hash", "")
token_total_hash = attribute_str("account", "TOKEN_TOTAL_HASH", "")
token_total_burial_hash = attribute_str("account", "TOKEN_TOTAL_BURIAL_HASH", "")
token_cookie_hash = attribute_str("account", "COOKIE_HASH", "")
token_zset = attribute_str("account", "TOKEN_ZSET", "")
token_hash = attribute_str("account", "TOKEN_HASH", "")
token_count_hash = attribute_str("account", "TOKEN_COUNT_HASH", "")
min_sleep = attribute_int("account", "MIN_SLEEP", 2)
burial_sleep = attribute_int("account", "BURIAL_SLEEP", 3600)
burial_times = attribute_int("account", "BURIAL_TIMES", 1000)
cookie_count = attribute_int("account", "COOKIE_COUNT", 1)

token_proxy_list = attribute_str("account", "TOKEN_PROXY", "").split(",")


login_token_account_hash = attribute_str("account", "login_token_account_hash", "")
cookie_total_hash = attribute_str("account", "cookie_total_hash", "")
cookie_total_zset = attribute_str("account", "cookie_total_zset", "")
cookie_total_count_hash = attribute_str("account", "cookie_total_count_hash", "")


user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.193 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.200 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.193 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.194 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.66 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.33 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.48 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.154 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.60 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.166 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.28 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.147 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.104 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.65 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36",
]


SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456qq@localhost:3306/DB_km"
SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
# db = SQLAlchemy(app)
cookies_redis_config = attribute_json("account", "COOKIE_REDIS_CONFIG", dict())
account_redis_client = CRedisHandler(host=cookies_redis_config['ip'], port=cookies_redis_config["port"], db=cookies_redis_config["db"],password=cookies_redis_config["password"])

DATA_DB_CONFIG = attribute_json("REDIS-DATA", "CONFIG", {})
data_redis_client = CRedisHandler(host=DATA_DB_CONFIG['ip'], port=DATA_DB_CONFIG["port"], db=DATA_DB_CONFIG["db"],password=DATA_DB_CONFIG["password"])

TASK_DB_CONFIG = attribute_json( "REDIS-TASK", "CONFIG", {})
task_redis_client = CRedisHandler(host=TASK_DB_CONFIG['ip'], port=TASK_DB_CONFIG["port"], db=TASK_DB_CONFIG["db"],password=TASK_DB_CONFIG["password"])
