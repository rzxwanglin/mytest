#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 16:46
# @Author  : dengyihong
# @Site    :
# @File    : redis_interface.py
# @Software: PyCharm

import json
from rhino_v2_utilis.handler.redis_handler import CRedisHandler


class CRedisFifoInterface(object):
    """
    右进左出redis队列 给任务队列和数据队列使用
    """

    task_redis_connector = None
    data_redis_connector = None

    @classmethod
    def init(cls, task_redis_config=None, data_redis_config=None):
        """
        :param task_redis_config:
        :param data_redis_config:
        :return:
        """
        if cls.task_redis_connector is None and task_redis_config is not None:
            cls.task_redis_connector = CRedisHandler(**task_redis_config)
        if cls.data_redis_connector is None and data_redis_config is not None:
            cls.data_redis_connector = CRedisHandler(**data_redis_config)

    @staticmethod
    def format_redis_list_data(data):
        """
        批量推入的列表数据成员是dict类型的，需要转换成str类型在批量入库
        """
        list_data = []
        if isinstance(data, dict):
            list_data.append(json.dumps(data))
        elif isinstance(data, list):
            list_data = data
        elif isinstance(data, str):
            list_data.append(data)

        list_string_data = []
        for one_data in list_data:
            if isinstance(one_data, str):
                list_string_data.append(one_data)
            else:
                list_string_data.append(json.dumps(one_data))
        return list_string_data

    @staticmethod
    def get_task_from_list(task_queue_name: str):
        """
        获取任务数据
        :params task_queue_name: 任务队列名
        :return: 字符串类型，任务信息
        """
        return CRedisFifoInterface.task_redis_connector.lpop(task_queue_name)

    @staticmethod
    def get_data_from_list(data_queue_name: str):
        """
        获取采集数据
        :params data_queue_name: 任务队列名
        :return: 字符串类型，任务信息
        """
        return CRedisFifoInterface.data_redis_connector.lpop(data_queue_name)

    @staticmethod
    def get_tasks_from_list(task_queue_name: str, count: int):
        """
        一次获取多个获取采集数据
        :params data_queue_name: 任务队列名
        :params count: 获取的数量
        :return: 返回获取的任务信息
        """
        return CRedisFifoInterface.task_redis_connector.batch_lpop_list(
            task_queue_name, count
        )

    @staticmethod
    def put_task_2_list(task_queue_name: str, json_task):
        """
        推送任务数据
        :params queue_name: 任务队列名
        :params json_task: 任务数据
        :return: True标识推送成功，False标识推送失败
        """

        return CRedisFifoInterface.task_redis_connector.rpush(
            task_queue_name, CRedisFifoInterface.format_redis_list_data(json_task)
        )

    @staticmethod
    def put_data_2_list(data_queue_name: str, json_data):
        """
        推送采集数据
        :params queue_name: 任务队列名
        :params json_task: 任务数据
        :return: True标识推送成功，False标识推送失败
        """
        return CRedisFifoInterface.data_redis_connector.rpush(
            data_queue_name, CRedisFifoInterface.format_redis_list_data(json_data)
        )
