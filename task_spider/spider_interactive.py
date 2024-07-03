
from loguru import logger
from config import task_redis_client
class SpiderInteractive(object):
    def __init__(self):
        logger.info('初始化instagram交互爬虫')


    def get_task(self):
        pass

    def get_handler(self):
        pass

    def run(self):
        while True:
            try:
                self.get_handler()
            except:
                pass






