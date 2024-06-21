#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/13 14:23
# @Author  : dengyihong
# @Site    :
# @File    : redis_pool.py
# @Software: PyCharm

import os
import sys
import logging
from redis import BlockingConnectionPool, SSLConnection


class CRedisPool(object):
    def __init__(
        self, host, port, db, password=None, pool_size=128, timeout=20, redis_ssl=False
    ):
        self.__m_str_host = host
        self.__m_port = port
        self.__m_str_password = password
        self.__m_db = db
        self.__m_pool_size = pool_size
        self.__m_timeout = timeout
        self.__m_obj_pool = None
        self.__redis_ssl = redis_ssl
        self.init()

    def __del__(self):
        if self.__m_obj_pool:
            try:
                self.__m_obj_pool.disconnect()
            except BaseException as base_err:
                print("free connection pool except:{0}".format(str(base_err)))

    def init(self):
        try:
            kwargs = {
                "max_connections": self.__m_pool_size,
                "timeout": self.__m_timeout,
                "host": self.__m_str_host,
                "port": self.__m_port,
                "password": self.__m_str_password,
                "db": self.__m_db,
                "socket_keepalive": True,
                "socket_timeout": 60,
                "socket_connect_timeout": 60,
                "retry_on_timeout": True,
                "decode_responses": True,
            }
            if self.__redis_ssl:
                pwd = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), os.path.pardir)
                )
                kwargs["connection_class"] = SSLConnection
                kwargs["ssl_keyfile"] = os.path.join(pwd, "certs", "redis", "redis.key")
                kwargs["ssl_certfile"] = os.path.join(
                    pwd, "certs", "redis", "redis.crt"
                )
                kwargs["ssl_ca_certs"] = os.path.join(pwd, "certs", "redis", "ca.crt")
            self.__m_obj_pool = BlockingConnectionPool(**kwargs)
        except BaseException as base_err:
            logging.error("create redis connection-pool failed.%s" % str(base_err))
            sys.exit(1)

    def get_redis_pool(self):
        return self.__m_obj_pool

    def return_connection(self, obj_connect):
        if not obj_connect:
            return False
        try:
            self.__m_obj_pool.release(obj_connect)
        except BaseException as base_err:
            logging.error(
                "return a connection to redis connection-pool except:{0}".format(
                    str(base_err)
                )
            )
            return False
        return True


if __name__ == "__main__":
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
