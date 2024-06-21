# -*-coding:utf-8 -*-
"""
# File       : dupefilter_interface.py
# Time       ：2022/7/7 10:09
# Author     ：caomengqi
# version    ：python 3.6
"""
from rhino_v2_utilis.config import ConfigHandler
from rhino_v2_utilis.handler.redis_handler import CRedisHandler
from rhino_v2_utilis.service.redis_bloom_interface import CRedisBloomInterface
from rhino_v2_utilis.settings import DUPEFILTER_REDIS_CONDIF


class CDupefilterHandler(object):
    interface_obj = None
    is_open = False

    @classmethod
    def init(cls, isopen: bool, dupefilter_redis_config: dict):
        """
        是否打开去重，用于设置可配置选项。
        为这个配设置静态的属性，加载一次后即可全局使用
        :param isopen:
        :param dupefilter_redis_config:传入的是redis的配置信息
        :return:
        """
        if not CDupefilterHandler.interface_obj and isopen:
            cls.interface_obj = CRedisBloomInterface(
                CRedisHandler(**dupefilter_redis_config)
            )
            cls.is_open = isopen

    @staticmethod
    def bloom_add(str_redis_key, value):
        """
        添加key
        添加时，如果存在会返回0 如果不存在，会返回1
        """
        if CDupefilterHandler.is_open:
            value = str(value) if isinstance(value, str) else value
            return CDupefilterHandler.interface_obj.bloom_add(str_redis_key, value)
        else:
            return 1

    @staticmethod
    def bloom_batch_add(str_redis_key, list_value):
        """
        添加key并且设置过期时间
        返回的内容  添加时存在返回0(添加失败) 不存在返回1(添加成功)
        返回两个列表 第一个是之前不存在，添加成功的  ，第二个是之前存在，也就是被去重的
        """
        if CDupefilterHandler.is_open:
            list_value = [str(i) for i in list_value]
            results = []
            repeated = []
            true_or_false = CDupefilterHandler.interface_obj.bloom_batch_add(
                str_redis_key, list_value
            )
            for i in range(len(list_value)):
                if true_or_false[i]:
                    results.append(list_value[i])
                else:
                    repeated.append(list_value[i])
            return results, repeated
        else:
            return

    @staticmethod
    def bloom_exist(str_redis_key, value):
        """
        判断是否在去重队列里面
        #没有key返回0  不存在返回0 存在返回1
        """
        if CDupefilterHandler.is_open:
            value = str(value) if isinstance(value, str) else value
            return CDupefilterHandler.interface_obj.bloom_exist(str_redis_key, value)
        else:
            return 0

    @staticmethod
    def bloom_batch_exist(str_redis_key, list_value):
        """
        判断是否存在
        通过布隆返回列表，对应的为1 是存在 为0 为不存在
        返回两个数据 第一个是存在的 第二个是不存在的
        """
        if CDupefilterHandler.is_open:
            results = []
            repeated = []
            list_value = [str(i) for i in list_value]
            true_or_false = CDupefilterHandler.interface_obj.bloom_batch_exist(
                str_redis_key, list_value
            )
            for i in range(len(list_value)):
                if true_or_false[i]:
                    repeated.append(list_value[i])
                else:
                    results.append(list_value[i])
            return repeated, results
        else:
            return [], list_value


DUPEFILTER_IS_OPEN = ConfigHandler.__get_property__("dupefilter", False)
# 初始化去重接口
if DUPEFILTER_IS_OPEN:
    CDupefilterHandler.init(
        isopen=DUPEFILTER_IS_OPEN, dupefilter_redis_config=DUPEFILTER_REDIS_CONDIF
    )

if __name__ == "__main__":
    DUPEFILTER_REDIS_CONDIF = {
        "host": "192.168.59.90",
        "port": 6380,
        "password": "surfilter@1218",
        "db": 2,
        "max_connections": 64,
        "capacity": 10000 * 10000,
        "rate": 0.0001 * 0.0001,
        "expire_day": 3 * 24 * 60 * 60,
    }
    CDupefilterHandler.init(True, **DUPEFILTER_REDIS_CONDIF)
    # status = CDupefilterHandler.bloom_add("skynet:twitter:user", str(1561351811531531531))
    # print(status)
    status = CDupefilterHandler.bloom_batch_exist(
        "skynet:twitter:user", ["cxasdcxsdcsd", "1564651303"]
    )
    print(status)
