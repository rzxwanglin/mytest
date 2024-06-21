# -*-coding:utf-8 -*-
"""
# File       : sche_interface.py
# Time       ：2022/6/1 11:42
# Author     ：caomengqi
# version    ：python 3.6
"""
# import config
import json
import time
import uuid
from copy import deepcopy
from typing import Union
from loguru import logger
from rhino_v2_utilis.handler.redis_handler import CRedisHandler
from rhino_v2_utilis.handler.task_handler import CTaskHandler
from rhino_v2_utilis.settings import TASK_REDIS_CONFIG


class CScheInterface:
    """
    和平台交互的模块，配合爬虫的日志模块使用
    """

    interface_enable = None
    interface_redis = None
    interface_schedule_max_buf = None

    @classmethod
    def init(cls, redis_task, schedule_enable=True, schedule_max_buf=409600):
        """
        判断是否是新平台
        """
        if not cls.interface_enable:
            CScheInterface.interface_enable = schedule_enable
        if not cls.interface_redis:
            CScheInterface.interface_redis = CRedisHandler(**redis_task)
        if not cls.interface_schedule_max_buf:
            CScheInterface.interface_schedule_max_buf = schedule_max_buf

    @staticmethod
    def llen(str_redis_key):
        return CScheInterface.interface_redis.llen(str_redis_key)

    @staticmethod
    def rpush(str_redis_key, value):
        return CScheInterface.interface_redis.rpush(str_redis_key, value)

    @staticmethod
    def send_msg_to_schd(
            json_task, type_value, val, task, msg: Union[str, int, dict] = "", **kwargs
    ):
        """
        params: task 任务信息
        params: type  msg_type           'add_task',  'resp',  'status',  'status',
        params: val value                   '',        '200',   'feth',  'finish',
        param: msg  在feth中设置爬取的数量    ''           ''        '1'       ''
        """
        schd_param = json_task.get("schd_param", None)
        if not schd_param or type_value not in [
            "status",
            "add_task",
            "exception",
            "resp",
            "alternative",
        ]:
            return False
        cp_schd_param = deepcopy(schd_param)
        cp_schd_param.pop("crawl", "")
        send_msg = {
            "schd_param": cp_schd_param,
            "msg_type": type_value,
            "value": val,
            "task": task,
            "msg": msg,
            "crawl_time": int(time.time()),
        }
        send_msg.update(**kwargs)
        inst_id = int(schd_param.get("iid", "0"))
        sid = int(schd_param.get("sid", "0"))
        if inst_id == 0 and sid == 0:
            lst = f"task_status:{json_task['task_info']['type']}"
        else:
            lst = f"task_status:{inst_id}:{sid}:{json_task['task_info']['type']}"
        len = CScheInterface.llen(lst)
        if len >= CScheInterface.interface_schedule_max_buf:
            # 达到最大值就不继续进行了
            logger.info(f"To schd buf is over,buf len:{lst}")
            return False
        else:
            CScheInterface.rpush(lst, json.dumps(send_msg))
            logger.info(json.dumps(send_msg))
            return True

    @staticmethod
    def change_sch_id(json_task: dict):
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        schd_param0 = deepcopy(schd_param)
        web_task_id = schd_param0["schd_task_id"].split(":")[0]
        schd_task_id = f"{web_task_id}:{str(uuid.uuid1())}"
        json_task["schd_param"]["schd_task_id"] = schd_task_id
        # 下面这一行很关键，不能缺少 加入 任务 状态
        json_task["schd_param"]["crawl"] = {"status": "add"}

    @staticmethod
    def sche_req(json_task: dict, task: str, **kwargs):
        """
        用于统计请求
        :params json_task：任务字段
        :params task:对应的采集项
        """
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        # if "crawl" in schd_param:
        #     st = schd_param["crawl"].get("status", None)
        #     if st == "add":
        #         return json_task
        CScheInterface.change_sch_id(json_task)
        CScheInterface.send_msg_to_schd(json_task, "add_task", "", task)
        if task == "images":
            estimate_size = kwargs.get("msg", 0)
            site_id = kwargs.get("site_id", -1)
            source = kwargs.get("source", 0)
            project = kwargs.get("project", ["hk01"])
            CScheInterface.send_msg_to_schd(
                json_task,
                type_value="alternative",
                val="estimate",
                task=task,
                msg=estimate_size,
                site=site_id,
                source=source,
                project=project,
            )
        return json_task

    @staticmethod
    def sche_res(json_task: dict, task: str, status: int):
        """
        用于统计请求
        :params json_task：任务字段
        :params task:对应的采集项
        :params status:状态码
        """
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        # 下面这一行很关键，不能缺少
        json_task["schd_param"]["crawl"] = {"status": "resp"}
        if status == 200:
            CScheInterface.send_msg_to_schd(json_task, "resp", str(status), task)
        return json_task

    @staticmethod
    def sche_pipe(json_task: dict, task: str, counts: int, **kwargs):
        """
        用于统计请求
        :params json_task：任务字段
        :params task:对应的采集项
        :params counts:爬取的数量
        :params site_id:站点id
        :params ld_volume:爬取的文件大小

        """
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task

        CScheInterface.send_msg_to_schd(
            json_task=json_task,
            type_value="status",
            val="fetch",
            task=task,
            msg=counts if counts else "",
            **kwargs,
        )
        CScheInterface.send_msg_to_schd(json_task, "status", "finish", task)

    @staticmethod
    def sche_exce(json_task: dict, task: str, error_value="Error"):
        """
        用于统计异常的响应
        :params json_task：任务字段
        :params task:对应的采集项
        """
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "exception", error_value, task)
        CScheInterface.send_msg_to_schd(json_task, "status", "finish", task)

    @staticmethod
    def sche_not_support(json_task: dict, task: str):
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "exception", "NotSupport", task)

    @staticmethod
    def sche_not_support_task(json_task: dict, task: str):
        if not CScheInterface.interface_enable:
            return json_task
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "exception", "NotSupportTask", task)

    @staticmethod
    def sche_redo(json_task: dict, delay: int = None):
        """
        给调度消息，这次的任务被我丢了，让调度过一会儿再下发
        防止任务积压在u
        Args:
            json_task:

        Returns: 是否REDO成功

        """
        if delay is None:
            delay = 1800
        if not CScheInterface.interface_enable:
            return False
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return False
        tasks = CTaskHandler.get_tasks(json_task)
        after = None
        for task in tasks:
            after = (
                CTaskHandler.get_task_limit(
                    json_task,
                )
                    .get(task, {})
                    .get("after")
            )
            if after:
                break
        if not after:
            return False
        return CScheInterface.send_msg_to_schd(
            json_task,
            type_value="exception",
            val="ReDo",
            task=None,
            msg={"delay": delay, "after": after},
        )

    @staticmethod
    def sche_following(json_task, task, **kwargs):
        if not CScheInterface.interface_enable:
            return
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "status", "Following", task)

    @staticmethod
    def sche_follow_succ(json_task, task, **kwargs):
        if not CScheInterface.interface_enable:
            return
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "status", "FollowSucc", task)

    @staticmethod
    def sche_need_bind(json_task, task, **kwargs):
        if not CScheInterface.interface_enable:
            return
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "status", "NeedBind", task)

    @staticmethod
    def sche_followfail(json_task, task):
        if not CScheInterface.interface_enable:
            return
        schd_param = json_task.get("schd_param", None)
        if not schd_param:
            return json_task
        CScheInterface.send_msg_to_schd(json_task, "status", "FollowFail", task)


# 初始化和调度交互接口
CScheInterface.init(TASK_REDIS_CONFIG)

if __name__ == '__main__':
    task_info = {
        "task_info": {
            "id": [
                "36266"
            ],
            "type": "twitter",
            "params": {
                "seed": [
                    "1288653700349571072"
                ],
                "seed_type": "user",
                "target_id": "228064",
                "timer": {
                    "interval": 21600,
                    "schedule_time": 1654599320
                },
                "crawl_image": False,
                "task": [
                    "post"
                ],
                "limit": {
                    "post": {
                        "count": -1,
                        "after": "2024-01-28 03:37:04 +0800"
                    }
                },
                "coll_ids": {
                    "post": 222135
                }
            }
        },
        "target_id": "228064",
        "priority": 3,
        "additional_information": {
            "start_time": "57600",
            "project": [
                "zc08"
            ]
        },
        "queue": "36266|twitter|user",
        "interface": "",
        "action": "add",
        "tag": "skynet",
        "schd_param": {
            "schd_task_id": "36266_6:1690664886",
            "father_id": "36266_6:1690664886",
            "schd_id": 6,
            "cycle_id": "1706385206",
            "stamp": 1706405864,
            "version": "4",
            "iid": 0,
            "sid": 2,
            "cid": "133000100"
        },
        "task_code": "418_zc08-3300-3400",
        "task_name": "418_zc08-3300-3400",
        "version": "4",
        "expire": 1706427464
    }

    CScheInterface.sche_following(task_info, task="post")
    CScheInterface.sche_follow_succ(task_info, task="post")
    CScheInterface.sche_followfail(task_info, task="post")
    CScheInterface.sche_pipe(task_info, task="post", counts=1, data_time=int(time.time()))
