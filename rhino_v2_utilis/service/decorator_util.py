#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/17 15:59
# @Author  : dengyihong
# @Site    :
# @File    : decorator_util.py
# @Software: PyCharm

import time
import traceback
import functools
from loguru import logger
from collections import defaultdict


def decorator_while_loop(func):
    """
    异常死循环捕获装饰器
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                ret = func(*args, **kwargs)
            except BaseException as base_err:
                logger.exception(base_err)
                # print(args, kwargs, func.__name__)
                time.sleep(1)
            else:
                return ret

    return wrapper


def always_while_func(error_sleep=0, sleep=30):
    """函数重复执行次数"""

    def always_decorator(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            while True:
                try:
                    func(*args, **kwargs)
                except BaseException as e:
                    logger.error(
                        f"function name : [ {func.__name__} ]; error : [ {str(e)} ]; "
                        f"args : [ {args} ]; kwargs : [ {kwargs} ]."
                    )
                    if not sleep:
                        continue
                    time.sleep(error_sleep)
                    traceback.print_exc()
                time.sleep(sleep)

        return wrapper_func

    return always_decorator


status_add_map = defaultdict(list)
status_rem_map = defaultdict(list)
dict_class_alive_hour = {}


def decorator_next_requests(func):
    """
    检测某个函数是否被执行的装饰器
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            class_hour = dict_class_alive_hour.get(args[0].__class__.__name__)
            current_hour = time.strftime("%Y-%m-%d %H", time.localtime(time.time()))
            if not class_hour or class_hour != current_hour:
                dict_class_alive_hour[args[0].__class__.__name__] = current_hour
                print(
                    "{}\tclass {} is alive.".format(
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                        args[0].__class__.__name__,
                    )
                )
            return func(*args, **kwargs)
        except Exception as e:
            print("decorator_next_requests error:{}".format(e))
            return

    return wrapper
