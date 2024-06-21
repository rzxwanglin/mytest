# -*-coding:utf-8 -*-
"""
# File       : config.py
# Time       ：2023/6/20 19:47
# Author     ：caomengqi
# version    ：python 3.6
"""
from inspect import isfunction


class ConfigHandler:
    site_type = "twitter"
    private_ip = None
    public_ip = None
    platform_port = 10443
    task_interface_type = "redis"  # redis or kafka
    data_interface_type = "redis"  # redis or kafka
    redis_ssl = False
    kafka_ssl = True
    dupefilter = False

    @classmethod
    def format(cls, **kwargs):
        for k, v in kwargs.items():
            setattr(cls, k, v)

    @classmethod
    def __get_property__(cls, property, value):
        """
        Args:
            property: 要获取的类属性
            value: 默认值
        Returns: 类属性 or 默认值
        """
        try:
            property_value = cls.__getattribute__(cls, property)
            # print(property, " : ", property_value, " : ", value)
            if property_value is not None:
                return property_value
        except AttributeError:
            pass
        if isfunction(value):
            return value()
        return value


if __name__ == "__main__":
    print(ConfigHandler.__get_property__("0", "00"))
    # print(ConfigHandler.__getattribute__("aaa", "bbb"))
    # ConfigHandler.format(**{"site_type": "telegram"})
    # print(ConfigHandler.__dict__)
    # print([{i: ConfigHandler.__dict__[i]} for i in ConfigHandler.__dict__ if not i.startswith("__")])
