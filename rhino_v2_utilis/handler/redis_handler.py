#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/13 14:23
# @Author  : dengyihong
# @Site    :
# @File    : redis_handler.py
# @Software: PyCharm
import redis
import logging
import datetime
from rhino_v2_utilis.service.redis_pool import CRedisPool
from rhino_v2_utilis.service.singleton_decorator import SingletonType
from rhino_v2_utilis.service.decorator_util import decorator_while_loop


# @singleton_decorator
class CRedisHandler(metaclass=SingletonType):
    """
    封装的redis 异常处理的核心 保证redis异常时不会出现问题
    """

    @decorator_while_loop
    def __init__(
            self,
            host="127.0.0.1",
            port=6379,
            password=None,
            db=0,
            max_connections=128,
            redis_ssl=False,
            *args,
            **kwargs
    ):
        self.__m_obj_redis = None
        self.__m_obj_pool = None
        self.__m_host = host
        self.__m_port = port
        self.__m_password = password
        self.__m_db = db
        self.__m_timeout = 10
        self.__m_pool_size = max_connections
        self.__m_redis_ssl = redis_ssl
        self.init()

    @decorator_while_loop
    def __del__(self):
        if self.__m_obj_redis:
            del self.__m_obj_redis
            pass
        if self.__m_obj_pool:
            del self.__m_obj_pool
        pass

    @decorator_while_loop
    def get_redis_pool(self):
        return self.__m_obj_pool.get_redis_pool()

    @decorator_while_loop
    def init(self,dict_argv :dict = {}):
        dict_argv = {
            "host": self.__m_host,
            "port": self.__m_port,
            "db": self.__m_db,
            "password": self.__m_password,
            "pool_size": self.__m_pool_size,
            "redis_ssl": self.__m_redis_ssl,
        }
        self.__m_obj_pool = CRedisPool(**dict_argv)


    @decorator_while_loop
    def lpush(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())

        if isinstance(value, list):
            obj_redis.lpush(str_redis_key, *value)
        else:
            obj_redis.lpush(str_redis_key, value)
        pass

    @decorator_while_loop
    def rpush(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())

        if isinstance(value, list):
            return obj_redis.rpush(str_redis_key, *value)
        else:
            return obj_redis.rpush(str_redis_key, value)
        pass

    @decorator_while_loop
    def llen(self, str_redis_key):
        list_len = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_len

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.llen(str_redis_key)

    @decorator_while_loop
    def lrange(self, str_redis_key, start_pos, end_pos):
        list_values = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_values

        if (
                (start_pos is None)
                or (end_pos is None)
                or not isinstance(start_pos, int)
                or not isinstance(end_pos, int)
        ):
            logging.error(
                "lrange start(%s) or end(%s) may be empty.",
                str(start_pos),
                str(end_pos),
            )
            return list_values

        if ((start_pos > 0) and (end_pos > 0) and (start_pos > end_pos)) or (
                (start_pos < 0) and (end_pos < 0) and (start_pos > end_pos)
        ):
            logging.error(
                "lrange start(%d) is greater than end(%d).", start_pos, end_pos
            )
            return list_values

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.lrange(str_redis_key, start=start_pos, end=end_pos)

    @decorator_while_loop
    def rpop(self, str_redis_key):
        value = None
        if not str_redis_key or not isinstance(str_redis_key, str):
            logging.error("redis key is incorrect.")
            return value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.rpop(str_redis_key)

    @decorator_while_loop
    def lpop(self, str_redis_key):
        value = None
        if not str_redis_key or not isinstance(str_redis_key, str):
            logging.error("redis key is incorrect.")
            return value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.lpop(str_redis_key)

    @decorator_while_loop
    def batch_rpop_list(self, str_redis_key, count):
        value = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            logging.error("redis key is incorrect.")
            return value

        if count is None or 0 >= count:
            logging.error("batch_pop count(%s) is incorrect.", str(count))
            return value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        # pop
        try:
            tmp_count = obj_redis.llen(str_redis_key)
            if tmp_count > count:
                tmp_count = count
                pass
            # with obj_redis.pipeline(transaction=False) as fp:
            with obj_redis.pipeline(transaction=True) as fp:
                while 0 < tmp_count:
                    fp.rpop(str_redis_key)
                    tmp_count -= 1
                    pass
                value = fp.execute()
                pass
        except BaseException as base_err:
            logging.error(
                "batch pop {0} {1} to redis failed.Except:{2}".format(
                    str_redis_key, str(value), str(base_err)
                )
            )
            return value
        # self.__m_obj_pool.ReturnConnect(obj_redis)
        return value

    @decorator_while_loop
    def batch_lpop_list(self, str_redis_key, count):
        value = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            logging.error("redis key is incorrect.")
            return value

        if count is None or 0 >= count:
            logging.error("batch_pop count(%s) is incorrect.", str(count))
            return value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        # pop
        try:
            tmp_count = obj_redis.llen(str_redis_key)
            if tmp_count > count:
                tmp_count = count
                pass
            # with obj_redis.pipeline(transaction=False) as fp:
            with obj_redis.pipeline(transaction=True) as fp:
                while 0 < tmp_count:
                    fp.lpop(str_redis_key)
                    tmp_count -= 1
                    pass
                value = fp.execute()
                pass
        except BaseException as base_err:
            logging.error(
                "batch pop {0} {1} to redis failed.Except:{2}".format(
                    str_redis_key, str(value), str(base_err)
                )
            )
            print(
                "batch pop {0} {1} to redis failed.Except:{2}".format(
                    str_redis_key, str(value), str(base_err)
                )
            )

            return value
        # self.__m_obj_pool.ReturnConnect(obj_redis)
        return value

    @decorator_while_loop
    def zadd(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        if not isinstance(value, dict):
            logging.error("value is not a dict type. it need dict ")
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zadd(str_redis_key, value)

    @decorator_while_loop
    def zrange_by_score(
            self,
            str_redis_key,
            min_score,
            max_score,
            start_pos=None,
            count=None,
            with_scores=False,
    ):
        """
        # 有序集合 返回的数据是有序的 小的在前面
        :param str_redis_key:
        :param min_score:
        :param max_score:
        :param start_pos:
        :param count:
        :param with_scores:
        :return:
        """
        list_values = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_values

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zrangebyscore(
            str_redis_key,
            min=min_score,
            max=max_score,
            start=start_pos,
            num=count,
            withscores=with_scores,
        )

    @decorator_while_loop
    def zrange(self, str_redis_key, start_pos, end_pos, desc=False, with_scores=False):
        list_values = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_values

        if (
                (start_pos is None)
                or (end_pos is None)
                or not isinstance(start_pos, int)
                or not isinstance(end_pos, int)
        ):
            logging.error(
                "zrange start(%s) or end(%s) may be empty.",
                str(start_pos),
                str(end_pos),
            )
            return list_values

        if ((start_pos > 0) and (end_pos > 0) and (start_pos > end_pos)) or (
                (start_pos < 0) and (end_pos < 0) and (start_pos > end_pos)
        ):
            logging.error(
                "zrange start(%d) is greater than end(%d).", start_pos, end_pos
            )
            return list_values

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zrange(
            str_redis_key,
            desc=desc,
            start=start_pos,
            end=end_pos,
            withscores=with_scores,
        )

    @decorator_while_loop
    def zrem(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zrem(str_redis_key, value)

    @decorator_while_loop
    def zscore(self, str_redis_key, value):
        score = None
        if not str_redis_key or not isinstance(str_redis_key, str):
            return score

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zscore(str_redis_key, value)

    # need redis v5.0.0
    @decorator_while_loop
    def zpopmin(self, str_redis_key, count=None):
        list_values = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_values

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zpopmin(str_redis_key, count=count)

    # need redis v5.0.0
    @decorator_while_loop
    def zpopmax(self, str_redis_key, count=None):
        list_values = []
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_values

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zpopmax(str_redis_key, count=count)

    @decorator_while_loop
    def sadd(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.sadd(str_redis_key, value)

    @decorator_while_loop
    def sismember(self, str_redis_key, value):
        is_member = False
        if not str_redis_key or not isinstance(str_redis_key, str):
            return is_member

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.sismember(str_redis_key, value)

    @decorator_while_loop
    def srem(self, str_redis_key, value):
        if not str_redis_key or not isinstance(str_redis_key, str):
            return False

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.srem(str_redis_key, value)

    @decorator_while_loop
    def spop(self, str_redis_key, count=None):
        str_value = ""
        if not str_redis_key or not isinstance(str_redis_key, str):
            return str_value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.spop(str_redis_key, count=count)

    @decorator_while_loop
    def scard(self, str_redis_key):
        count = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return count

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.scard(str_redis_key)

    @decorator_while_loop
    def hgetall(self, str_redis_key):
        dict_key_value = {}
        if not str_redis_key or not (
                isinstance(str_redis_key, str) or isinstance(str_redis_key, bytes)
        ):
            return dict_key_value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hgetall(str_redis_key)

    @decorator_while_loop
    def hscan(self, str_redis_key, str_match_expr):
        dict_key_value = {}
        cursor = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return dict_key_value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        count = 0
        try:
            while True:
                # print cursor
                # tp_result = obj_redis.hscan(str_redis_key, cursor = cursor, match = str_match_expr, count = 1)
                tp_result = obj_redis.hscan(
                    str_redis_key, cursor=cursor, match=str_match_expr
                )
                cursor = tp_result[0]
                if 0 == cursor:
                    break
                else:
                    count += len(tp_result[1])
                    dict_key_value.update(tp_result[1])
                pass
        except BaseException as base_err:
            logging.error(
                "hscan {0} to redis failed.Except:{1}".format(
                    str_redis_key, str(base_err)
                )
            )
            return dict_key_value
        return dict_key_value

    @decorator_while_loop
    def hget(self, str_redis_key, str_field):
        str_value = ""
        if not str_redis_key or not isinstance(str_redis_key, str):
            return str_value

        if not str_field or not (
                isinstance(str_field, str) or isinstance(str_field, bytes)
        ):
            return str_value

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hget(str_redis_key, str_field)

    @decorator_while_loop
    def hkeys(self, str_redis_key):
        list_keys = ""
        if not str_redis_key or not isinstance(str_redis_key, str):
            return list_keys

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hkeys(str_redis_key)

    @decorator_while_loop
    def hexists(self, str_redis_key, str_field):
        ret = 0
        if not str_redis_key or not isinstance(str_field, str):
            return ret
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hexists(str_redis_key, str_field)

    @decorator_while_loop
    def hset(self, str_redis_key, str_field, str_value):
        ret = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hset(str_redis_key, str_field, str_value)

    @decorator_while_loop
    def hdel(self, str_redis_key, str_field):
        ret = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hdel(str_redis_key, str_field)

    @decorator_while_loop
    def hvals(self, str_redis_key):
        ret = 0
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hvals(str_redis_key)

    @decorator_while_loop
    def keys(self, pattern):
        list_keys = list()

        if not pattern or not isinstance(pattern, str):
            return list_keys

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.keys(pattern)

    @decorator_while_loop
    def type(self, redis_key):
        key_type = None

        if not redis_key or not isinstance(redis_key, str):
            return key_type

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.type(redis_key)

    @decorator_while_loop
    def set_key_expire(self, str_redis_key, expire_time):
        state = False
        if not str_redis_key or not isinstance(str_redis_key, str):
            return state

        if expire_time is None or not (
                isinstance(expire_time, int)
                or isinstance(expire_time, float)
                or isinstance(expire_time, datetime.timedelta)
        ):
            return state

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.expire(str_redis_key, expire_time)

    @decorator_while_loop
    def hincrby(self, str_redis_key, str_field, count):
        state = None
        if not str_redis_key or not isinstance(str_redis_key, str):
            return state

        if not str_field or not isinstance(str_field, str):
            return state

        if count is None or not isinstance(count, int):
            return state

        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.hincrby(str_redis_key, str_field, count)

    def zincrby(self, str_redis_key, str_field, count):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zincrby(str_redis_key, str_field, count)

    @decorator_while_loop
    def exists(self, str_redis_key):
        ret = False
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.exists(str_redis_key)

    @decorator_while_loop
    def get(self, str_redis_key):
        value = None
        if not str_redis_key or not isinstance(str_redis_key, str):
            return value
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.get(str_redis_key)

    @decorator_while_loop
    def set(self, str_redis_key, value, expire_time=None):
        # TODO redis set 设置的值 不需要限制类型
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.set(str_redis_key, value, ex=expire_time)

    @decorator_while_loop
    def incr(self, str_redis_key, amount=1):
        ret = False
        if (
                not str_redis_key
                or not isinstance(str_redis_key, str)
                or not amount
                or not isinstance(amount, int)
        ):
            return ret
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.incr(str_redis_key, amount)

    @decorator_while_loop
    def delete(self, str_redis_key):
        ret = False
        if not str_redis_key or not isinstance(str_redis_key, str):
            return ret
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.delete(str_redis_key)

    @decorator_while_loop
    def ping(self):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.ping()

    @decorator_while_loop
    def zcard(self, redis_key):
        if not redis_key or not isinstance(redis_key, str):
            return 0
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.zcard(redis_key)

    @decorator_while_loop
    def pipeline(self):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.pipeline()

    @decorator_while_loop
    def execute_command(self, *args, **options):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.execute_command(*args, **options)

    @decorator_while_loop
    def blpop(self, redis_key, timeout):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.blpop(redis_key, timeout)

    @decorator_while_loop
    def brpop(self, redis_key, timeout):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.brpop(redis_key, timeout)

    @decorator_while_loop
    def ttl(self, redis_key):
        obj_redis = redis.Redis(connection_pool=self.__m_obj_pool.get_redis_pool())
        return obj_redis.ttl(redis_key)