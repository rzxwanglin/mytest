# -*-coding:utf-8 -*-
import threading
import time, random, json, copy, datetime, os
from loguru import logger
import setproctitle, traceback, requests
import config
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from rhino_v2_utilis.config import ConfigHandler

from task_spider.spider_interactive import  SpiderInteractive
from task_spider.spider_data import SpiderData
from utilis.distribution_task import DistributionTask

logger.add(
    './var/log/instagram/output.log',
    retention="3 days",
    rotation="100 MB",
    format="{message}",
    encoding="utf-8",
    enqueue=False,
)


if __name__ == "__main__":
    logger.info('run')
    threading.Thread(target=DistributionTask().run, args=()).start()
    threading.Thread(target=SpiderInteractive().run, args=()).start()
    threading.Thread(target=SpiderData().run, args=()).start()

    #todo 消费db2 持久化mysql



