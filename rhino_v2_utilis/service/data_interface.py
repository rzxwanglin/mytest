#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 17:08
# @Author  : dengyihong
# @Site    :
# @File    : data_interface.py
# @Software: PyCharm

import json
from rhino_v2_utilis.config import ConfigHandler
from rhino_v2_utilis.service.decorator_util import decorator_while_loop
from rhino_v2_utilis.settings import DATA_REDIS_CONFIG


class CDataInterface(object):
    interface_obj = None

    @staticmethod
    def init(DATA_REDIS_CONFIG, **kwargs):
        """
        根据参数识别是哪种队列（比如：redis、kafka），实例化队列链接接口
        """
        print(kwargs.get("type"), DATA_REDIS_CONFIG)
        if kwargs.get("type") == "redis":
            from rhino_v2_utilis.service.redis_interface import CRedisFifoInterface

            CRedisFifoInterface.init(data_redis_config=DATA_REDIS_CONFIG)
            CDataInterface.interface_obj = CRedisFifoInterface
        elif kwargs.get("type") == "kafka" and CDataInterface.interface_obj is None:
            from rhino_v2_utilis.service.kafka_interface import CKafkaInterface

            CKafkaInterface.init(data_config=DATA_REDIS_CONFIG)
            CDataInterface.interface_obj = CKafkaInterface
        else:
            print("配置的data_interface_type出现问题")

    @staticmethod
    @decorator_while_loop
    def push_data(data_queue_name: str, json_data):
        """
        推送采集数据
        :params data_queue_name: 任务队列名
        :params json_task: 任务数据
        :return: 字符串类型，任务信息
        """

        if isinstance(json_data, dict):
            json_data = json.dumps(json_data, sort_keys=True)
        return CDataInterface.interface_obj.put_data_2_list(data_queue_name, json_data)

    @staticmethod
    @decorator_while_loop
    def get_data(data_queue_name):
        """
        获取数据
        :params data_queue_name: 任务队列名
        :return: 字符串类型，任务信息
        """
        return CDataInterface.interface_obj.get_data_from_list(data_queue_name)


CDataInterface.init(
    DATA_REDIS_CONFIG,
    type=ConfigHandler.__get_property__("data_interface_type", "redis"),
)
