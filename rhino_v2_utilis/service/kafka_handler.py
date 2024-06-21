# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     kafka_handler.py  
   Description :  
   Author :        Duckweeds7
   date：           2022/8/15
-------------------------------------------------
   Change Activity:
                   2022/8/15: 
-------------------------------------------------
"""
__author__ = "Duckweeds7"

import configparser
import functools
import json
import os
import random
import socket
import sys
import threading
import time
import uuid
import platform
from loguru import logger
from functools import wraps
from os.path import basename
from confluent_kafka import KafkaError, Producer, Consumer
from concurrent.futures import ThreadPoolExecutor

PRODUCER_KEY_LIST = ["bootstrap.servers", "retries"]
CONSUMER_KEY_LIST = [
    "bootstrap.servers",
    "group.id",
    "enable.auto.commit",
    "auto.offset.reset",
]

client_id = socket.gethostname()


def ack(err, msg):
    """
    默认的回调函数，err非空是代表推送出现错误
    msg.value().decode() 为推送的数据
    :param err:
    :param msg:
    :return:
    """
    try:
        topic = msg.topic()
        data = json.loads(msg.value().decode())
        if err is not None:
            logger.warning(f"push {topic} raise a {err} error!")
        else:
            logger.debug(f"push {topic} succeed!")
    except Exception as e:
        logger.error(f"function ack raise a {e} error, err:{err}, msg:{msg}")


def singleton(cls):
    _instance = {}

    def inner(*args, **argv):
        if cls not in _instance:
            _instance[cls] = cls(*args, **argv)
        return _instance[cls]

    return inner


def log_cast_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        result = func(*args, **kw)
        end = time.time()
        if result:
            logger.debug("funciton: {}, 消耗时长为：{}".format(func.__name__, end - start))
        return result

    return wrapper


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if "ip" in kwargs or "host" in kwargs:
            kwargs[
                "bootstrap.servers"
            ] = f"{kwargs.get('ip', '') or kwargs.get('host', '')}:{kwargs.get('port', 9092)}"
        if "bootstrap.servers" in kwargs:
            instance_key = "kafka-{}".format(kwargs.get("bootstrap.servers"))
        elif "config" in kwargs:
            instance_key = "kafka-{}".format(basename(kwargs.get("config")))
        else:
            instance_key = "instance"

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
                print("kafka__new__")
        return cls._instance.get(instance_key)


def decorator_while_loop(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                count = func(*args, **kwargs)
            except BaseException as base_err:
                logger.exception(base_err)
                time.sleep(1)
                continue
            else:
                return count

    return wrapper


class CKafkaHandler(metaclass=SingletonType):
    @decorator_while_loop
    def __init__(self, **kwargs):
        self.executor = ThreadPoolExecutor(max_workers=1080)
        self.batch_size = 1
        self.write_instances = {}
        self.read_instances = {}
        self.read_config = {
            "bootstrap.servers": "127.0.0.1:9092",
            "group.id": uuid.uuid1(),
            "enable.auto.commit": True,
            "auto.offset.reset": "earliest",
        }
        # self.write_config = {"bootstrap.servers": "127.0.0.1:9092", "retries": 30}
        self.write_config = {
            "bootstrap.servers": "127.0.0.1:9092",
            "compression.codec": "snappy",
            "batch.num.messages": 10000,
            "request.required.acks": 1,
            "message.max.bytes": 20 * 1024 * 1024,
            "batch.size": 20 * 1024 * 1024,
        }
        if kwargs.get("kafka_ssl"):
            pwd = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.path.pardir)
            )
            self.read_config["security.protocol"] = "SSL"
            self.read_config["ssl.ca.location"] = os.path.join(
                pwd, "certs", "kafka", "CARoot.pem"
            )
            self.read_config["ssl.certificate.location"] = os.path.join(
                pwd, "certs", "kafka", "certificate.pem"
            )
            self.read_config["ssl.key.location"] = os.path.join(
                pwd, "certs", "kafka", "key.pem"
            )
            if platform.system() == "Darwin":
                self.write_config["enable.ssl.certificate.verification"] = False
            self.write_config["security.protocol"] = "SSL"
            self.write_config["ssl.ca.location"] = os.path.join(
                pwd, "certs", "kafka", "CARoot.pem"
            )
            self.write_config["ssl.certificate.location"] = os.path.join(
                pwd, "certs", "kafka", "certificate.pem"
            )
            self.write_config["ssl.key.location"] = os.path.join(
                pwd, "certs", "kafka", "key.pem"
            )

        self.callback = ack
        if "config" in kwargs:
            self.config_path = kwargs.get("config")
            if not self.read_params():
                sys.exit(1)
        else:
            for k, v in kwargs.items():  # 对参数进行遍历 如果有生产者或消费者的配置参数时传入
                if k in PRODUCER_KEY_LIST:
                    self.write_config[k] = v
                if k in CONSUMER_KEY_LIST:
                    self.read_config[k] = v

    @decorator_while_loop
    def read_params(self):
        """
        从传的config参数路径的cfg文件读取配置信息
        :return:
        """
        obj_config = configparser.ConfigParser()
        try:
            obj_config.read(self.config_path)
            self.write_config.update(json.loads(obj_config.get("KAFKA-DATA", "CONFIG")))
            self.read_config.update(json.loads(obj_config.get("KAFKA-TASK", "CONFIG")))

        except BaseException as base_err:
            logger.error("new a kafka instance failed.except:{0}".format(str(base_err)))
            return False
        return True

    @decorator_while_loop
    def get_data(self, consumer):
        """
        根据后续可能任务从kafka读取的角度设计,默认读的数量为1条,并且返回序列化后的数据,若大于1则返回序列化后的列表
        :param consumer:
        :return:
        """
        items = {} if self.batch_size == 1 else []
        msgs = consumer.consume(num_messages=self.batch_size, timeout=0.5)
        for msg in msgs:
            if msg.error():
                if msg.error().code() == KafkaError.PARTITION_EOF:
                    return items
                elif msg.error():
                    logger.exception(
                        "kafka reade data error, instance:{}, topic:{}, partition:{}, reason:{}".format(
                            consumer, msg.topic(), msg.partition(), msg.error()
                        )
                    )
                    return items
            else:
                value = msg.value().decode()
                item = json.loads(value) if isinstance(value, str) else value
                if self.batch_size == 1:
                    items = item
                    return items
                else:
                    items.append(item)
        return items

    @decorator_while_loop
    def save_data(self, topic, item, instance):
        """
        写kafka的具体操作
        :param topic:
        :param item:
        :param instance:
        :return:
        """
        if not item:
            return
        data = item if isinstance(item, str) else json.dumps(item)
        instance.produce(topic, value=data, callback=self.callback)

    @decorator_while_loop
    def consumer(self, config, topic):  # 根据topic创建消费者对象
        consumer = Consumer(**config)
        consumer.subscribe([topic])
        return consumer

    @decorator_while_loop
    def producer(self, config):  # 根据topic创建生产者对象 一个topic对应100个生产者
        config["client.id"] = client_id
        producer = [Producer(**config) for i in range(1)]
        return producer

    @decorator_while_loop
    def get_consumer(self, topic):  # 根据topic获取对应的消费者对象
        if not self.read_instances.get(topic):
            instance = self.read_instance(self.read_config, topic)
            self.read_instances[topic] = instance
        else:
            instance = self.read_instances[topic]
        return instance

    @decorator_while_loop
    def get_producer(self, topic):  # 根据topic随机获取对应的生产者对象
        if not self.write_instances.get(topic):
            instance = self.write_instance(self.write_config)
            print(self.write_config)
            self.write_instances[topic] = instance
        else:
            instance = self.write_instances[topic]
        return instance

    @decorator_while_loop
    def read_instance(self, config, topic):
        return self.consumer(config, topic)

    @decorator_while_loop
    def write_instance(self, config):
        return self.producer(config)

    @decorator_while_loop
    def read_with_instance(self, instance):
        items = self.get_data(instance)
        return items

    @decorator_while_loop
    def write_with_instance(self, topic, items, instance):
        """
        :param topic:
        :param items:
        :param instance:
        :return:
        """
        if isinstance(instance, list):
            instance = random.choice(instance)
        if isinstance(items, str):
            items = [json.loads(items)]
        elif isinstance(items, dict):
            items = [items]
        elif isinstance(items, list):
            items = list(
                map(
                    lambda item: json.loads(item) if isinstance(item, str) else item,
                    items,
                )
            )
        for item in items:
            self.save_data(topic, item, instance)
        instance.flush()  # 会导致阻塞的操作 kafka应用层的回调是通过三方库api实现的，需要执行flush操作才能得知信息发生的成功与失败
        # self.executor.submit(instance.flush)

    @log_cast_time
    @decorator_while_loop
    def read(self, topic):
        topic = topic.replace(":", "-")
        instance = self.get_consumer(topic)
        items = self.read_with_instance(instance)
        return items

    @log_cast_time
    @decorator_while_loop
    def write(self, topic, items):
        topic = topic.replace(":", "-")
        instance = self.get_producer(topic)
        self.write_with_instance(topic, items, instance)
        return True

    @decorator_while_loop
    def exists(self, topic):
        """
        是否存在该topic
        :param topic: 查询的topic
        :return: boolean True/False
        """
        topic = topic.replace(":", "-")
        instance = self.get_consumer(topic)
        if topic in instance.list_topics().topics.keys():
            return True
        else:
            return False
