#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 17:07
# @Author  : dengyihong
# @Site    :
# @File    : task_interface.py
# @Software: PyCharm

import json
from loguru import logger
import time
from rhino_v2_utilis.handler.redis_handler import CRedisHandler
from rhino_v2_utilis.handler.task_handler import CTaskHandler
from rhino_v2_utilis.service.decorator_util import decorator_while_loop
from rhino_v2_utilis.service.redis_interface import CRedisFifoInterface
from rhino_v2_utilis.settings import TASK_REDIS_CONFIG
from rhino_v2_utilis.handler.rhino_v2_platform_api import RhinoV2Api


class CTaskInterface(object):
    interface_obj = None
    delete_task = dict()
    sync_time = dict()

    @staticmethod
    def init(TASK_REDIS_CONFIG, **kwargs):
        """
        根据参数识别是哪种队列（比如：redis、kafka），实例化队列链接接口
        """
        """
        if is redis:
            CTaskInterface.interface_obj = redis interface
        elif is kafka:
            CTaskInterface.interface_obj = kafka interface
        """
        if not CTaskInterface.interface_obj:
            CRedisFifoInterface.init(task_redis_config=TASK_REDIS_CONFIG)
            CTaskInterface.interface_obj = CRedisFifoInterface

    @staticmethod
    @decorator_while_loop
    def push_task(task_queue_name: str, json_task: dict):
        """
        推送采集数据
        :params task_queue_name: 任务队列名
        :params json_task: 任务数据
        :return: 字符串类型，任务信息
        """
        if json_task.get("priority") and str(json_task.get("priority")) == "1":
            task_queue_name = "priority-1:" + task_queue_name
        return CTaskInterface.interface_obj.put_task_2_list(
            task_queue_name, json_task if isinstance(json_task, str) else json.dumps(json_task)
        )

    @staticmethod
    def sync_stop_info(tag: str):
        """
        读取redis中的停止任务信息(每30s同步一次)
        :tag :str
        """
        crruent_time = time.time()
        if crruent_time - CTaskInterface.sync_time.get(tag, 0) >= 30:
            if not CTaskInterface.delete_task.get(tag):
                CTaskInterface.delete_task[tag] = set()
            redis_key = f"crawl:stop:{RhinoV2Api.m_cluster_id}:{tag}:{RhinoV2Api.m_site_type}"
            datas = CRedisHandler(**TASK_REDIS_CONFIG).zrange(redis_key, 0, -1)
            for data in datas:
                if isinstance(data, str):
                    data = json.loads(data)
                if data.get("action") == "stop" and data.get("schd_task_id") and data.get("version"):
                    CTaskInterface.delete_task[tag].add(f'stop:{data.get("schd_task_id")}:{data.get("version")}')
            CTaskInterface.sync_time[tag] = crruent_time

    @staticmethod
    def get_task(task_queue_name: str):
        """
        推送采集数据
        :params task_queue_name: 任务队列名
        :return: dict类型，任务信息
        """
        if not task_queue_name:
            return
        task_info = CTaskInterface.interface_obj.get_task_from_list("priority-1:" + task_queue_name) or \
                    CTaskInterface.interface_obj.get_task_from_list(task_queue_name)
        return CTaskInterface.translate(task_queue_name, task_info)

    @staticmethod
    def get_tasks(task_queue_name: str, count: int):
        """
        推送采集数据
        :params task_queue_name: 任务队列名
        :params count: 需要获取的任务数量
        :return: 列表内的为dict类型，任务信息
        """
        results = []
        if not task_queue_name or not count:
            return results
        datas = CTaskInterface.interface_obj.get_tasks_from_list("priority-1:" + task_queue_name, count) or \
                CTaskInterface.interface_obj.get_tasks_from_list(task_queue_name, count)
        for data in datas:
            data = CTaskInterface.translate(task_queue_name, data)
            if data:
                results.append(data)
        return results

    @staticmethod
    def translate(task_queue_name, task_info):
        """
        转换的工具函数，把从redis返回的内容转换为dict
        :params task_info: 从redis返回的任务信息
        :return: 转换后的数据源内容
        """
        try:
            if isinstance(task_info, str):
                task_info = json.loads(task_info)
            elif isinstance(task_info, bytes):
                task_info = json.loads(task_info.decode("UTF-8"))
            elif isinstance(task_info, dict):
                pass
            else:
                # logging.error('unsupported task_info type: {}'.format(str(type(task_info))))
                task_info = {}
            father_id = CTaskHandler.get_father_id(task_info)  # 此处是 father_id 而不是 schd_task_id
            version = CTaskHandler.get_version(task_info)
            tag = CTaskHandler.get_task_tag(task_info)
            site_type = CTaskHandler.get_site_type(task_info)
            expire = task_info.get("expire", 0)
            if tag and task_queue_name.endswith(site_type) and expire and isinstance(expire, int) and expire < int(
                    time.time()):
                logger.info(f"task is expire : {json.dumps(task_info)}")
                return {}
            CTaskInterface.sync_stop_info(tag)
            if father_id and version \
                    and CTaskInterface.delete_task.get(tag) \
                    and f'stop:{father_id}:{version}' in CTaskInterface.delete_task.get(tag):
                logger.info(f"task is deleted : {json.dumps(task_info)}")
                task_info = {}
        except BaseException as base_err:
            logger.exception(base_err)
            task_info = {}
        return task_info


CTaskInterface.init(TASK_REDIS_CONFIG)

if __name__ == "__main__":
    CTaskInterface.init(TASK_REDIS_CONFIG)
    CTaskInterface.get_tasks("skynet:twitter:liked", 20)
