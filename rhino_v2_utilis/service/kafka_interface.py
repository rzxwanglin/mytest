# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     kafka_interface.py  
   Description :  
   Author :        Duckweeds7
   date：           2022/8/18
-------------------------------------------------
   Change Activity:
                   2022/8/18: 
-------------------------------------------------
"""
__author__ = "Duckweeds7"

from rhino_v2_utilis.service.kafka_handler import CKafkaHandler


class CKafkaInterface(object):
    task_kafka_connector = None
    data_kafka_connector = None

    @classmethod
    def init(cls, task_config=None, data_config=None):
        """

        :param data_config: 传入的是字典
        :return:
        """
        if cls.data_kafka_connector is None and data_config:
            cls.data_kafka_connector = CKafkaHandler(**data_config)
        if cls.task_kafka_connector is None and task_config:
            cls.task_kafka_connector = CKafkaHandler(**task_config)

    @staticmethod
    def get_task_from_list(task_queue_name):
        """
        获取任务数据
        :params task_queue_name: 任务队列名
        :return:dict类型，任务信息
        """
        return CKafkaInterface.task_kafka_connector.read(task_queue_name)

    @staticmethod
    def get_data_from_list(data_queue_name):
        """
        获取采集数据
        :params data_queue_name: 任务队列名
        :return: 字符串类型，任务信息
        """
        return CKafkaInterface.data_kafka_connector.read(data_queue_name)

    @staticmethod
    def put_task_2_list(task_queue_name, json_task):
        """
        推送任务数据
        :params queue_name: 任务队列名
        :params json_task: 任务数据
        :return: True标识推送成功，False标识推送失败
        """
        return CKafkaInterface.task_kafka_connector.write(task_queue_name, json_task)

    @staticmethod
    def put_data_2_list(data_queue_name, json_data):
        """
        推送采集数据
        :params queue_name: 任务队列名
        :params json_task: 任务数据
        :return: True标识推送成功，False标识推送失败
        """
        return CKafkaInterface.data_kafka_connector.write(data_queue_name, json_data)
