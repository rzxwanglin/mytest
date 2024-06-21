#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/13 15:10
# @Author  : dengyihong
# @Site    :
# @File    : singleton_decorator.py
# @Software: PyCharm

import threading


def singleton(cls):
    _instance = {}

    def inner(*args, **argv):
        if cls not in _instance:
            _instance[cls] = cls(*args, **argv)
        return _instance[cls]

    return inner


class SingletonType(type):
    """
    保证redis 连接池的单例 使当前进程中只创建一次 redis 连接池
    """

    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if "host" in kwargs:
            instance_key = "{}-{}-{}".format(
                kwargs.get("host"), kwargs.get("port"), kwargs.get("db")
            )
        elif "ip" in kwargs:
            instance_key = "{}-{}-{}".format(
                kwargs.get("ip"), kwargs.get("port"), kwargs.get("db_name")
            )
        else:
            instance_key = "instance"
            pass

        with SingletonType._instance_lock:
            if not hasattr(cls, "_instance"):
                if not hasattr(cls, "_instance"):
                    cls._instance = (
                        {}
                    )  # super(SingletonType,cls).__call__(*args, **kwargs)
            if instance_key not in cls._instance:
                cls._instance[instance_key] = super(SingletonType, cls).__call__(
                    *args, **kwargs
                )
                print("__new__")
        return cls._instance.get(instance_key)
