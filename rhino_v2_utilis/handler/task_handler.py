#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 16:40
# @Author  : dengyihong
# @Site    :
# @File    : task_handler.py
# @Software: PyCharm

import json
import time
from datetime import datetime, timezone, timedelta

from dateutil import tz


class CTaskHandler(object):

    @classmethod
    def get_schd_task_id(cls, json_task: dict):
        return CTaskHandler.get_schd_param(json_task).get('schd_task_id', "")

    # father_id
    @classmethod
    def get_father_id(cls, json_task: dict):
        return CTaskHandler.get_schd_param(json_task).get('father_id', "")

    @classmethod
    def get_version(cls, json_task: dict):
        return str(json_task.get('version', "0"))

    @classmethod
    def get_schd_param(cls, json_task: dict):
        return json_task.get('schd_param', {})

    @staticmethod
    def get_first_distribution(json_task: dict):
        if json_task.get("first_distribution", None):
            json_task["first_distribution"] = int(time.time())
        return json_task.get("first_distribution", int(time.time()))

    @staticmethod
    def get_action(json_task: dict):
        return json_task.get("action", "")

    @staticmethod
    def get_task_info(json_task: dict):
        return json_task.get("task_info", {})

    @staticmethod
    def get_task_id(json_task: dict):
        task_info = CTaskHandler.get_task_info(json_task)
        return task_info.get("id") if task_info else ""

    @staticmethod
    def get_site_type(json_task: dict):
        task_info = CTaskHandler.get_task_info(json_task)
        return task_info.get("type") if task_info else ""

    @staticmethod
    def get_seed_type(json_task: dict):
        params = CTaskHandler.get_params(json_task)
        return params.get("seed_type", "") if params else ""

    @staticmethod
    def get_task_tag(json_task: dict):
        return json_task.get("tag", "")

    @staticmethod
    def get_site_id(json_task: dict):
        additional_info = CTaskHandler.get_additional_info(json_task)
        site_id = additional_info.get("site_id")
        return site_id if site_id else -1

    @staticmethod
    def get_site_name(json_task: dict):
        additional_info = CTaskHandler.get_additional_info(json_task)
        site_name = additional_info.get("site_name")
        return site_name if site_name else "unknown"

    @staticmethod
    def get_remark(json_task: dict):
        additional_info = CTaskHandler.get_additional_info(json_task)
        remark = additional_info.get("remark")
        return remark if remark else ""

    @staticmethod
    def get_additional_info(json_task: dict):
        return json_task.get("additional_information", {})

    @staticmethod
    def get_lbs(json_task: dict):
        info = CTaskHandler.get_additional_info(json_task)
        return info.get("lbs", {}) if info else {}

    @staticmethod
    def get_project(json_task: dict):
        info = CTaskHandler.get_additional_info(json_task)
        return info.get("project", []) if info else []
        pass

    @staticmethod
    def get_params(json_task: dict):
        task_info = CTaskHandler.get_task_info(json_task)
        return task_info.get("params") if task_info else {}

    @staticmethod
    def get_seed(json_task: dict):
        params = CTaskHandler.get_params(json_task)
        return params.get("seed", []) if params else []

    @staticmethod
    def get_current_url(json_task: dict):
        current_url = json_task.get("current_url")
        return current_url if current_url else CTaskHandler.get_seed(json_task)

    @staticmethod
    def get_rules_list(json_task: dict):
        return json_task.get("rules_list", {})

    @staticmethod
    def get_current_rule_id(json_task: dict):
        additional_info = CTaskHandler.get_additional_info(json_task)
        return additional_info.get("next_rule_id") if additional_info else -1

    @staticmethod
    def get_execution_order(json_task: dict):
        additional_info = CTaskHandler.get_additional_info(json_task)
        return additional_info.get("execution_order") if additional_info else []

    @staticmethod
    def get_current_rule(json_task: dict):
        rule_list = CTaskHandler.get_rules_list(json_task)
        rule = (
            rule_list.get(str(CTaskHandler.get_current_rule_id(json_task)))
            if rule_list
            else {}
        )
        rule = rule if rule else {}
        return rule

    @staticmethod
    def serialization_task(task):
        json_task = None
        if isinstance(task, bytes) or isinstance(task, str):
            try:
                json_task = json.loads(task)
            except BaseException as base_err:
                print("format task<<<{}>>> except:{}".format(task, base_err))
                json_task = None
        elif isinstance(task, dict):
            json_task = task
        return json_task

    @staticmethod
    def get_temp_seed(json_task: dict):
        # return CTaskHandler.get_params(json_task).get('temp_seed')
        return json_task.get("temp_seed")

    @staticmethod
    def set_temp_seed(list_temp_seed: list, json_task: dict):
        if not isinstance(list_temp_seed, list):
            return
        # dict_params = CTaskHandler.get_params(json_task)
        # dict_params['temp_seed'] = list_temp_seed
        json_task["temp_seed"] = list_temp_seed  # TODO 应该没有使用
        pass

    @staticmethod
    def get_task_timer(json_task: dict):
        params = CTaskHandler.get_params(json_task)
        return params.get("timer", {}) if params else {}

    @staticmethod
    def get_task_limit(json_task: dict):
        params = CTaskHandler.get_params(json_task)
        return params.get("limit", {}) if params else {}

    @staticmethod
    def parse_time_zone(timeval):
        a = datetime.strptime(timeval, "%Y-%m-%d %H:%M:%S %z")
        tz_gmt = tz.tzoffset(None, 0)
        return a.astimezone(tz_gmt)

    @staticmethod
    def get_before_after_count(data_dict, name):
        before = "3000-05-21 14:21:14 +0800"
        before = CTaskHandler.parse_time_zone(before).timestamp()
        task_limit = CTaskHandler.get_task_limit(data_dict)
        after = task_limit.get(name, {}).get("after") or "1000-05-21 14:21:14 +0800"
        after = CTaskHandler.parse_time_zone(after).timestamp()
        count = task_limit.get(name, {}).get("count", -1)
        return before, after, count

    @staticmethod
    def compare_time(before, after, create_at):
        # print(before, after, create_at)
        return after <= create_at <= before

    @staticmethod
    def get_post_limit_time(json_task: dict, time_type: str = "before"):
        format_time = (
            CTaskHandler.get_task_limit(json_task).get("post", {}).get(time_type)
        )
        if not format_time:
            return datetime.now().timestamp()
        else:
            datetime_obj = datetime.strptime(format_time, "%Y-%m-%d %H:%M:%S %z")
        return datetime_obj.timestamp()

    @staticmethod
    def set_post_limit_time(json_task: dict, timestamp: int, time_type: str = "before"):
        post_limit_time = CTaskHandler.get_task_limit(json_task).get("post", {})
        datetime_obj = datetime.fromtimestamp(timestamp)
        datetime_obj = datetime_obj.astimezone(timezone(timedelta(hours=0)))
        date_string_with_timezone = datetime_obj.strftime("%Y-%m-%d %H:%M:%S %z")
        post_limit_time[time_type] = date_string_with_timezone
        pass

    @staticmethod
    def get_tasks(json_task: dict):
        params = CTaskHandler.get_params(json_task)
        return params.get("task", {}) if params else {}

    @staticmethod
    def get_access_token(json_task: dict):
        return json_task.get("access_token", "")

    @staticmethod
    def get_source_seed(json_task: dict):
        return json_task.get("source_seed", [])

    @staticmethod
    def set_source_seed(json_task: dict, source_seed):
        # return CTaskHandler.get_params(json_task).get('temp_seed')
        json_task["source_seed"] = source_seed
        pass

    @staticmethod
    def get_penetrate_task_id(json_task: dict):
        """
        获取渗透任务的ID
        :params json_task: 任务信息
        :return: 任务队列名
        """
        info = CTaskHandler.get_additional_info(json_task)
        return info.get("penetrate_task_id") if info else None

    @staticmethod
    def get_task_queue_name(json_task: dict, task_name: str, access_token: dict = None):
        """
        获取任务的队列名
        :params json_task: 任务信息
        :params task_name: 任务名
        :params access_token: 采集账号信息
        :return: 任务队列名
        """
        internet_ip = ""
        if access_token and CTaskHandler.get_penetrate_task_id(json_task):
            internet_ip = access_token.get("internet_ip")
            task_queue_format = (
                "%(internet_ip)s:%(task_tag)s:%(site_type)s:%(task_name)s"
            )

        else:
            task_queue_format = "%(task_tag)s:%(site_type)s:%(task_name)s"
            pass
        task_queue = task_queue_format % {
            "internet_ip": internet_ip,
            "task_tag": CTaskHandler.get_task_tag(json_task),
            "site_type": CTaskHandler.get_site_type(json_task),
            "task_name": task_name,
        }
        return task_queue

    @staticmethod
    def get_add_tasks(json_task: dict):
        info = CTaskHandler.get_additional_info(json_task)
        return info.get("tasks", []) if info else []

    @staticmethod
    def get_source(json_task: dict):
        tasks = CTaskHandler.get_add_tasks(json_task)
        return 0 if not tasks else tasks[0].get("source", 0)

    @staticmethod
    def get_src_task_id(json_task: dict):
        tasks = CTaskHandler.get_add_tasks(json_task)
        return "" if not tasks else tasks[0].get("taskId", "")
