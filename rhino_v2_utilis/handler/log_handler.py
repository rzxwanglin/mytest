# -*-coding:utf-8 -*-
"""
# File       : log_handler.py
# Time       ：2023/6/21 11:27
# Author     ：caomengqi
# version    ：python 3.6
"""
import copy
import json
from copy import deepcopy
from datetime import datetime
from loguru import logger
from rhino_v2_utilis.config import ConfigHandler
from rhino_v2_utilis.handler.rhino_v2_platform_api import RhinoV2Api
from rhino_v2_utilis.service.sche_interface import CScheInterface
from rhino_v2_utilis.handler.task_handler import CTaskHandler
from rhino_v2_utilis.settings import TASK_REDIS_CONFIG
from rhino_v2_utilis.handler.json_handler import JsonHandle
from rhino_v2_utilis.service.redis_interface import CRedisHandler


def format_log(task_info, msg, task, logging_type, **kwargs):
    """
     格式化日志和上传新爬虫管理平台某些内容
    :params task_info 任务信息
    :params msg 日志附加信息
    :params task 和任务中匹配的采集项  如果不能匹配，在下面的上传状态模块需要做映射进行匹配
    :logging_type 过程的状态
    :kwargs 附加的内容和信息
    """
    if kwargs.pop("not_upload", None):
        return
    if "tag" not in task_info and "source_seed" not in task_info:  # 兼容层级
        task_info = task_info.get("task_info", {})
    project = (
        task_info.get("additional_information", {}).get("project", [])
        or task_info.get("source_task", {})
        .get("additional_information", {})
        .get("project", [])
        or []
        if task_info
        else {}
    )
    # 上传状态
    try:
        if logging_type == "request":
            CScheInterface.sche_req(
                json_task=task_info, task=task_info.get("crawl_task", task)
            )
            # logger.error(f"<---------------- source_task_name::{source_task_name} | {logging_type} ------------------->")
        elif logging_type == "response" and not kwargs.get("error_code", None):
            CScheInterface.sche_res(
                json_task=task_info,
                task=task_info.get("crawl_task", task),
                status=kwargs.get("status", 0),
            )
            # logger.error(f"<---------------- source_task_name:{source_task_name} | {logging_type} ------------------->")
        elif logging_type == "alternative":
            CScheInterface.send_msg_to_schd(
                json_task=task_info,
                type_value="alternative",
                val="estimate",
                task=task,
                msg=kwargs.get("estimate_size", 0),
                site=kwargs.get("site_id", 0) or CTaskHandler.get_site_id(task_info),
                source=kwargs.get("source", 0) or CTaskHandler.get_source(task_info),
                project=project,
            )
            # logger.error(f"<---------------- source_task_name:{source_task_name} | {logging_type} ------------------->")
        elif logging_type == "pipelines":
            CScheInterface.sche_pipe(
                json_task=task_info,
                task=task_info.get("crawl_task", task),
                counts=kwargs.get("counts", 1),
                kwargs=kwargs
            )
            # logger.error(f"<---------------- source_task_name::{source_task_name} | {logging_type} ------------------->")
        elif logging_type == "exception":
            CScheInterface.sche_exce(
                json_task=task_info, task=task_info.get("crawl_task", task)
            )
            if not kwargs.get("error"):
                kwargs["error"] = {"code": 255, "description": "未知错误"}
            # logger.error(f"<---------------- source_task_name::{source_task_name} | {logging_type} ------------------->")
        elif logging_type == "nopipelines":
            CScheInterface.sche_pipe(
                json_task=task_info,
                task=task_info.get("crawl_task", task),
                counts=0,
            )
            if not kwargs.get("error"):
                kwargs["error"] = {"code": 255, "description": "未知错误"}
        else:
            pass
    except BaseException as e:
        pass

    schd_param = task_info.get("schd_param", {})
    if schd_param:
        schd_param_deep_copy = deepcopy(schd_param)
        schd_param_deep_copy.pop("crawl", "")
        kwargs["schd_param"] = schd_param_deep_copy
    temp_seed = task_info.get("temp_seed", []) or []
    format_msg = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 日志生成时间
        "msg": msg,
        "msg_type": ConfigHandler.__get_property__("msg_type", None)
                    or f"{RhinoV2Api.m_site_type}",
        # 消息类型,标识索引,爬虫可以用自己的爬虫名,调度用调度名如: scheduler
        "batch_id": CTaskHandler.get_task_id(task_info),  # 对应新版调度的临时job_id
        "temp_seed": temp_seed or CTaskHandler.get_seed(task_info),  # 本次任务对应的种子有哪些
        "type": f"{RhinoV2Api.m_site_type}",  # 日志格式统一规范定义里没有这个字段,可用来标识是哪个爬虫的设置状态的日志
        "seed_type": CTaskHandler.get_seed_type(
            task_info
        ),  # 任务的种子类型，比如：user、page、group、keyword等
        "tag": CTaskHandler.get_task_tag(task_info),
        "logging_type": logging_type,
        "task": task
        if task
        else CTaskHandler.get_tasks(task_info),  # 如果是设置状态或调度的日志 该字段设为空值
        "source_seed": CTaskHandler.get_source_seed(task_info) or CTaskHandler.get_seed(task_info),  # 任务的源种子
        "ip_address": RhinoV2Api.m_public_ip,
        "seed": CTaskHandler.get_seed(task_info),
        "project": CTaskHandler.get_project(task_info)
        if CTaskHandler.get_task_tag(task_info)
        else [],
        "cluster_id": RhinoV2Api.m_cluster_id,
        "private_ip": RhinoV2Api.m_private_ip,
        "crawl_task": task_info.get("crawl_task", ""),
        "after": CTaskHandler.get_task_limit(task_info)
        .get(task_info.get("crawl_task", "") or task, {})
        .get("after", "")
        if task_info.get("crawl_task", "") or task
        else CTaskHandler.get_task_limit(task_info).get("post", {}).get("after")
             or CTaskHandler.get_task_limit(task_info).get("search", {}).get("after", ""),
    }
    # kwargs 中需要加以下参数
    # error_token_id
    # token_id
    # status
    # counts pipeline时会使用
    # proxy 没有的话为 空字符串
    tasks_list = JsonHandle.helper_dict("tasks", task_info)
    if (
            JsonHandle.helper_dict("task_info", task_info)
            and JsonHandle.helper_dict("task_info", task_info).get("type", "") == "media"
            and tasks_list != None
    ):
        tasks = tasks_list[0]
        batch_id = (
            JsonHandle.helper_dict("raw_task", tasks).get("task_info", {}).get("id", "")
            if JsonHandle.helper_dict("raw_task", tasks)
            else CTaskHandler.get_task_id(task_info)
        )
        source_seed = tasks.get("raw_task", {}).get("source_seed", []) or tasks.get(
            "raw_task", {}
        ).get("task_info", {}).get("params", {}).get("seed", [])
        format_msg.update(
            {
                "data_type": JsonHandle.helper_dict("task_info", task_info).get(
                    "type", ""
                ),
                "user_id": tasks.get("userId", ""),
                "post_id": tasks.get("postId")
                if tasks.get("postId")
                else tasks.get("album_id", ""),
                "temp_seed": JsonHandle.helper_dict("params", task_info).get("seed")[0],
                "batch_id": batch_id if isinstance(batch_id, list) else [batch_id],
                "type": f"{RhinoV2Api.m_site_type}",
                "crawl_task": tasks.get("crawl_task")
                if tasks.get("crawl_task")
                else task_info.get("crawl_task", ""),
                "source_seed": source_seed,
            }
        )

    format_msg.update(kwargs)
    if ConfigHandler.__get_property__("log_to_redis", False):
        CRAWL_LOG_CONFIG = copy.deepcopy(TASK_REDIS_CONFIG)
        CRAWL_LOG_CONFIG["db"] = 11
        log_client = CRedisHandler(**CRAWL_LOG_CONFIG)
        log_client.rpush(
            "facebook_crawler_logging", json.dumps(format_msg, ensure_ascii=False)
        )
    logger.info(json.dumps(format_msg, ensure_ascii=False))
