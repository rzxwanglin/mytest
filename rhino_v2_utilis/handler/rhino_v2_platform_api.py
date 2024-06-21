#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/13 14:23
# @Author  : dengyihong
# @Site    :
# @File    : rhino_v2_platform_api.py
# @Software: PyCharm
# @dec     : 和平台的交互
import json
import time
from loguru import logger
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
import random

from rhino_v2_utilis.handler.task_handler import CTaskHandler
from rhino_v2_utilis.handler.util import (
    download_web,
    modify_api_dict,
    get_private_ip,
    get_public_ip,
)
from rhino_v2_utilis.config import ConfigHandler
from rhino_v2_utilis.service.decorator_util import always_while_func

from rhino_v2_utilis.service.decorator_util import decorator_while_loop

disable_warnings()


class RhinoV2Api(object):
    m_domain = ""
    m_port = 10443
    m_username = ""
    m_password = ""
    m_access_token_uri = ""
    m_penetration_task_state_uri = ""
    m_penetration_task_token_map_uri = ""
    m_cluster_interface_uri = ""
    m_heart_beat_uri = ""
    m_enable_new_platform = False
    m_access_header = None
    m_http_basic_auth = None
    m_task_interface_params = None
    m_data_interface_params = None
    m_project_list = None
    m_private_ip = ""
    m_public_ip = ""
    m_max_buf = None
    m_site_type = ""
    platform_proxy = None
    m_cluster_id = -1

    @classmethod
    def init(cls):
        """
        初始化函数
        # :param config:配置文件
        :return:
        """
        # cls.m_domain = "https://crawler.skynet001.com"
        cls.m_domain = ConfigHandler.__get_property__(
            "platform_domain", "https://crawler.skynet001.com"
        )
        cls.m_port = ConfigHandler.__get_property__("platform_port", 10443)
        cls.m_username = "root"
        cls.m_password = "surfilter@1218"
        cls.m_enable_new_platform = ConfigHandler.__get_property__("new_platform", True)
        cls.m_access_token_uri = "/api/2.0/get/token"
        cls.m_penetration_task_state_uri = (
            "/api/2.0/set/penetration_task/token_seed/status"
        )
        cls.m_penetration_task_token_map_uri = "/api/2.0/get/token_seed/mapping"
        cls.m_cluster_interface_uri = "/api/2.0/cluster/interface_info"
        cls.m_heart_beat_uri = "/api/2.0/cluster/node/heart/beat/upload"
        cls.m_max_buf = ConfigHandler.__get_property__("max_buf", 409600)
        cls.m_site_type = ConfigHandler.__get_property__("site_type", "telegram")
        if cls.m_enable_new_platform is True:
            cls.m_http_basic_auth = None
            cls.m_access_header = {
                "access_token": ConfigHandler.__get_property__("access_token", "e710ec70-dd8a-4842-a1a6-20478c8f9fe5"),
                "Content-Type": "application/json",
            }
        else:
            cls.m_http_basic_auth = HTTPBasicAuth(cls.m_username, cls.m_password)
            cls.m_access_header = {"Content-Type": "application/json"}
        cls.m_private_ip = ConfigHandler.__get_property__("private_ip", get_private_ip)
        cls.m_public_ip = ConfigHandler.__get_property__("public_ip", get_public_ip)
        cls.platform_proxy = ConfigHandler.__get_property__("platform_proxy", [])
        cls.m_cluster_id = ConfigHandler.__get_property__("cluster_id", -1)
        cls.get_cluster_info()
        cls.database_info()

    @classmethod
    def database_info(cls):
        task_ssl = False
        task_database_config = {}
        task_type = cls.m_task_interface_params.get("type", "redis")
        add_json = cls.m_task_interface_params.get("addJson")
        if add_json:
            try:
                task_json = json.loads(add_json)
                task_ssl_verify = task_json.get("verify", False)
                if task_ssl_verify:
                    task_ssl = True
            except:
                pass
        if task_type and task_type == "redis":
            task_database_config = {
                "task_interface_type": task_type,
                "task_redis_ssl": task_ssl
            }
        elif task_type and task_type == "kafka":
            task_database_config = {
                "task_interface_type": task_type,
                "task_kafka_ssl": task_ssl
            }
        ConfigHandler.format(**task_database_config)
        data_ssl = False
        data_database_config = {}
        data_type = cls.m_data_interface_params.get("type", "redis")
        add_json = cls.m_data_interface_params.get("addJson")
        if add_json:
            try:
                data_json = json.loads(add_json)
                data_ssl_verify = data_json.get("verify", False)
                if data_ssl_verify:
                    data_ssl = True
            except:
                pass
        if data_type and data_type == "redis":
            data_database_config = {
                "data_interface_type": data_type,
                "data_redis_ssl": data_ssl
            }
        elif task_type and task_type == "kafka":
            data_database_config = {
                "data_interface_type": data_type,
                "data_kafka_ssl": data_ssl
            }
        ConfigHandler.format(**data_database_config)

    @classmethod
    def choice_proxy(cls):
        if not cls.platform_proxy or not isinstance(cls.platform_proxy, list):
            return None
        proxy = (
            random.choice(cls.platform_proxy)
                .strip()
                .strip("https://")
                .strip("http://")
                .strip("/")
        )
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    @classmethod
    def format_url(cls, uri):
        if not cls.m_port:
            return "{}{}".format(cls.m_domain, uri)
        else:
            return "{}:{}{}".format(cls.m_domain, cls.m_port, uri)

    @classmethod
    def get_penetrate_task_account(cls, seed_type: str = "user", seed: str = ""):
        """
        获取渗透任务种子及其绑定access_token的关系函数
        :param seed_type: 种子类型
        :param seed: 种子
        :return: True标识成功，False标识失败
        """

        url = cls.format_url(cls.m_penetration_task_token_map_uri)
        dict_params = {
            "type": cls.m_site_type,  # 表示应用类型
            "seed_type": seed_type,  # 种子类型
            "seed": seed,  # 种子
        }
        response = download_web(
            open_url=url,
            method="GET",
            dict_headers=cls.m_access_header,
            dict_params=dict_params,
            data=None,
            dict_proxies=cls.choice_proxy(),
            verify=False,
            timeout=20,
            auth=cls.m_http_basic_auth,
        )
        if response and 200 == response.status_code:
            json_data = json.loads(response.text)
            return json_data.get("data", {}).get("list", [])
        else:
            return []

    @classmethod
    def report_merge_account(cls, payload: str):
        """
        facebook 爬虫专用，上报合并账号信息
        """
        url = cls.format_url("/api/2.0/addCombinedAccount")  # 合并账号上传接口
        response = download_web(
            open_url=url,
            method="POST",
            dict_headers=cls.m_access_header,
            data=payload,
            dict_proxies=cls.choice_proxy(),
            verify=False,
            timeout=20,
            auth=cls.m_http_basic_auth,
        )
        if response and 200 == response.status_code:
            json_data = json.loads(response.text)
            return json_data.get("data", {}).get("list", [])
        else:
            return []

    @classmethod
    def set_token_status(cls, dict_token: dict, token_status: int = -1):
        """
        上传渗透任务种子异常状态函数
        :param dict_token: twitter token的有效信息
        :param token_status: twitter token的有效信息，状态为失效 (1,表示有效， 0，表示失效， -1 ，表示账号还活着，但是渗透失败,种子和token关系不存在了)
        :return: True标识成功，False标识失败
        """
        if not dict_token or token_status not in [0, 1]:
            return False

        url = cls.format_url("/api/2.0/set_token_invalid")
        if cls.m_enable_new_platform:
            dict_params = {
                "access_token": dict_token.get("access_token"),
                "state": token_status,
                "account_id": dict_token.get("account_id"),
            }
        else:
            dict_params = {
                "access_token": dict_token.get("access_token"),
                "state": token_status,
            }

        response = download_web(
            open_url=url,
            method="GET",
            dict_headers=cls.m_access_header,
            dict_params=dict_params,
            data=None,
            dict_proxies=cls.choice_proxy(),
            verify=False,
            timeout=20,
            auth=cls.m_http_basic_auth,
        )
        if not response:
            logger.info(
                "update access_token_secret:{access_token}, account_id {account_id},status:{state} failed".format(
                    **{
                        "access_token": dict_token["access_token"],
                        "state": token_status,
                        "account_id": dict_token.get("account_id"),
                    }
                )
            )
            return False
        else:
            logger.info(
                "update access_token_secret:{access_token}, account_id {account_id} ,status:{state} sucessful".format(
                    **{
                        "access_token": dict_token["access_token"],
                        "state": token_status,
                        "account_id": dict_token.get("account_id"),
                    }
                )
            )
            return True
        pass

    @classmethod
    def get_token(cls, token_status: int = 1, count=200):
        """
        获取采集账号
        :param count: 获取的账号数量
        :param token_status: twitter token的有效信息，状态为失效 (1,表示有效， 0，表示失效)
        :return: 响应信息。格式："{\"code\":0,\"msg\":\"success\",\"data\":{\"list\":[]}}"
        """
        url = cls.format_url(cls.m_access_token_uri)

        dict_params = {
            "internet_ip": cls.m_public_ip,
            "type": cls.m_site_type,
            "state": token_status,
            "intranet_ip": cls.m_private_ip,
            "count": count,
        }
        response = download_web(
            open_url=url,
            method="GET",
            dict_headers=cls.m_access_header,
            dict_params=dict_params,
            data=None,
            dict_proxies=cls.choice_proxy(),
            verify=False,
            timeout=20,
            auth=cls.m_http_basic_auth,
        )
        if not response or 200 != response.status_code:
            logger.error(
                f"get node:{cls.m_public_ip} {cls.m_site_type}'s access_token failed."
            )
            return "{}"
        else:
            logger.info(
                f"get node:{cls.m_public_ip} {cls.m_site_type}'s access_token success."
            )
            return response.text
        pass

    @classmethod
    @always_while_func(sleep=58, error_sleep=12)
    def heart_beat(cls):
        """
        做一个心跳包，告诉爬虫管理平台，这个节点的爬虫正常工作运行
        """
        data_body = {
            "site_type": cls.m_site_type,
            "internet_ip": cls.m_public_ip,
            "intranet_ip": cls.m_private_ip,
        }
        url = cls.format_url(cls.m_heart_beat_uri)
        response = download_web(
            open_url=url,
            method="POST",
            dict_headers=cls.m_access_header,
            data=json.dumps(data_body),
            verify=False,
            timeout=20,
            auth=cls.m_http_basic_auth,
            dict_proxies=cls.choice_proxy(),
        )
        if not response:
            logger.error(f"heart_beat:{cls.m_public_ip} {cls.m_site_type}'s  failed.")
            return False
        else:
            return True

    @classmethod
    @decorator_while_loop
    def get_cluster_info(cls):
        """
        获取节点所属集群的配置信息
        :return:
        """
        task_host = ConfigHandler.__get_property__("task_host", None)
        task_port = ConfigHandler.__get_property__("task_port", None)
        task_password = ConfigHandler.__get_property__("task_password", None)
        task_db = ConfigHandler.__get_property__("task_db", None)
        data_host = ConfigHandler.__get_property__("data_host", None)
        data_port = ConfigHandler.__get_property__("data_port", None)
        data_db = ConfigHandler.__get_property__("data_db", None)
        data_password = ConfigHandler.__get_property__("data_password", None)
        project_list = ConfigHandler.__get_property__("project_list", None)
        if task_host and task_port and data_host and data_port and project_list:
            cls.m_task_interface_params = {
                "ip": task_host,
                "port": task_port,
                "db_name": task_db,
                "password": task_password,
            }
            cls.m_data_interface_params = {
                "ip": data_host,
                "port": data_port,
                "db_name": data_db,
                "password": data_password,
            }
            cls.m_project_list = project_list
            return
        url = cls.format_url(cls.m_cluster_interface_uri)

        dict_params = {
            "internet_ip": cls.m_public_ip,
            "intranet_ip": cls.m_private_ip,
            "type": cls.m_site_type,
        }

        while True:
            config_list = (
                {
                    "ip": "127.0.0.1",
                    "db_name": "1",
                    "password": "",
                    "port": "6379",
                    "decode_responses": True
                },
                {
                    "ip": "127.0.0.1",
                    "db_name": "0",
                    "password": "",
                    "port": "6379",
                    "decode_responses": True
                },
                #
                # {
                #     "ip": "10.11.204.20",
                #     "db_name": "1",
                #     "password": "surfilter@1218",
                #     "port": "6380",
                #     "decode_responses": True
                # },
                # {
                #     "ip": "10.11.204.20",
                #     "db_name": "0",
                #     "password": "surfilter@1218",
                #     "port": "6380",
                #     "decode_responses": True
                # },
                ["skynet", "baggio", "data_center", "warning", "neymar","gb"],
            )
            cls.m_task_interface_params = config_list[1]
            cls.m_data_interface_params = config_list[0]
            cls.m_project_list = config_list[2]
            cls.m_cluster_id = 33
            break
            response = download_web(
                open_url=url,
                method="GET",
                dict_headers=cls.m_access_header,
                dict_params=dict_params,
                data=None,
                dict_proxies=cls.choice_proxy(),
                verify=False,
                timeout=20,
                auth=cls.m_http_basic_auth,
            )
            if not response or 200 != response.status_code:
                logger.error(
                    f"get node:{cls.m_public_ip}:{cls.m_private_ip}  {cls.m_site_type}'s interface param failed."
                )
                time.sleep(5)
                continue
            else:
                config_list = json.loads(response.text).get("data", {}).get("list", [])
                if config_list:
                    cls.m_data_interface_params = modify_api_dict(
                        config_list[0]["data_interface_info"]
                    )
                    cls.m_task_interface_params = modify_api_dict(
                        config_list[0]["task_interface_info"]
                    )
                    cls.m_project_list = config_list[0].get("project_list")
                    cls.m_cluster_id = config_list[0].get('clusterId', -1)
                else:
                    logger.error(
                        f"parse node:{cls.m_public_ip}:{cls.m_private_ip} {cls.m_site_type}'s interface param failed."
                    )
                    time.sleep(5)
                    continue
                print(cls.m_task_interface_params)
                print(cls.m_data_interface_params)
                print(cls.m_project_list)
                break

    @staticmethod
    def update_seed_state(dict_task, msg="Sorry, that page does not exist."):
        """
        上传种子异常状态函数
        :param dict_task: 任务信息
        :param msg: 任务中种子的异常描述信息
        :return: True标识成功，False标识失败
        """
        if not dict_task:
            return False
        url = RhinoV2Api.format_url("/api/1.0/tasks/state")
        source_seed = CTaskHandler.get_source_seed(dict_task)
        source_seed = (
            source_seed[0] if 1 == len(source_seed) else json.dumps(source_seed)
        )
        payload = json.dumps(
            {
                "site_type": CTaskHandler.get_site_type(dict_task),
                "seed": source_seed,
                "state": "error",
                "task_id": CTaskHandler.get_task_id(dict_task),
                "access_token": CTaskHandler.get_access_token(dict_task),
                "msg": msg,
            }
        )

        response = download_web(
            open_url=url,
            method="POST",
            dict_headers=RhinoV2Api.m_access_header,
            dict_params=None,
            data=payload,
            dict_proxies=None,
            verify=False,
            timeout=20,
            auth=RhinoV2Api.m_http_basic_auth,
        )
        if not response:
            return False
        else:
            return True
        pass

    @staticmethod
    def notify_penetrate_task_status(json_task, token_status=-1):
        """
        上传渗透任务种子异常状态函数
        :param json_task: 任务信息
        :param token_status: twitter token的有效信息，状态为失效 (1,表示有效， 0，表示失效， -1 ，表示账号还活着，但是渗透失败,种子和token关系不存在了)
        :return: True标识成功，False标识失败
        """
        if not json_task:
            return False
        access_token = json_task.get("token")
        if not CTaskHandler.get_penetrate_task_id(json_task) or not isinstance(
                access_token, dict
        ):
            return False

        url = RhinoV2Api.format_url(RhinoV2Api.m_penetration_task_state_uri)

        payload = json.dumps(
            {
                "type": RhinoV2Api.m_site_type,  # 表示应用类型
                "seed_type": CTaskHandler.get_seed_type(json_task),  # 种子类型
                "seed": CTaskHandler.get_source_seed(json_task)[0],  # 种子
                "token_id": access_token.get("token_id", -1),  # token的自增id
                "status": token_status,
            }
        )

        response = download_web(
            open_url=url,
            method="POST",
            dict_headers=RhinoV2Api.m_access_header,
            dict_params=None,
            data=payload,
            dict_proxies=None,
            verify=False,
            timeout=20,
            auth=RhinoV2Api.m_http_basic_auth,
        )
        if not response:
            return False
        else:
            return True
        pass


RhinoV2Api.init()
