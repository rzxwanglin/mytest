# -*-coding:utf-8 -*-
"""
# File       : dupefilter_interface.py
# Time       ：2022/7/7 10:09
# Author     ：caomengqi
# version    ：python 3.6
"""

from redisbloom.client import Client
from rhino_v2_utilis.service.decorator_util import decorator_while_loop


class CRedisBloomInterface:
    def __init__(self, redis_pool, **argv):
        self.__m_capacity = 10000000
        self.__m_error_rate = 0.0001
        self.__m_expire_day = 2 * 86400
        try:
            self.__m_capacity = argv.get("capacity", 10000000)
            self.__m_error_rate = argv.get("rate", 0.0001)
            self.__m_expire_day = argv.get("expire_day", 2 * 86400)
        except:
            pass
        self.redis = redis_pool
        self.redis_pool = redis_pool.get_redis_pool()
        self.__m_filter_redis_key = set([])

    @decorator_while_loop
    def bloom_create_key(self, str_redis_key):
        ret = False
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret

        obj_redis = Client(connection_pool=self.redis_pool)
        if not self.redis.exists(str_redis_key):
            ret = obj_redis.bfCreate(
                str_redis_key,
                errorRate=self.__m_error_rate,
                capacity=self.__m_capacity,
            )
            ret |= self.redis.set_key_expire(str_redis_key, self.__m_expire_day)
        else:
            ret = True
        return ret

    @decorator_while_loop
    def bloom_add(self, str_redis_key, value):
        if (
                not str_redis_key
                or not isinstance(str_redis_key, str)
                or not value
                or not isinstance(value, str)
        ):
            return False
        self.bloom_create_key(str_redis_key)
        obj_redis = Client(connection_pool=self.redis_pool)
        return obj_redis.bfAdd(str_redis_key, value)

    @decorator_while_loop
    def bloom_exist(self, str_redis_key, value):
        if (
                not str_redis_key
                or not isinstance(str_redis_key, str)
                or not value
                or not isinstance(value, str)
        ):
            return False

        obj_redis = Client(connection_pool=self.redis_pool)
        return obj_redis.bfExists(str_redis_key, value)

    @decorator_while_loop
    def bloom_batch_add(self, str_redis_key, list_value):
        if (
                not str_redis_key
                or not isinstance(str_redis_key, str)
                or not list_value
                or not isinstance(list_value, list)
        ):
            return []
        self.bloom_create_key(str_redis_key)
        obj_redis = Client(connection_pool=self.redis_pool)
        return obj_redis.bfMAdd(str_redis_key, *list_value)

    @decorator_while_loop
    def bloom_batch_exist(self, str_redis_key, list_value):
        if (
                not str_redis_key
                or not isinstance(str_redis_key, str)
                or not list_value
                or not isinstance(list_value, list)
        ):
            return []

        obj_redis = Client(connection_pool=self.redis_pool)
        return obj_redis.bfMExists(str_redis_key, *list_value)
