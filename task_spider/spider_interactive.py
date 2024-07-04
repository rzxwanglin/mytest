import time
import requests
from loguru import logger
from config import task_redis_client
from utilis.account_redis_interface import AccountRedisInterface
from request_factory import RequestFactory
class SpiderInteractive(object):
    def __init__(self):
        logger.info('初始化instagram交互爬虫')

    def get_task(self):
        while True:
            task_info = task_redis_client.lpop('instagram:task')
            if task_info:
                break
            else:
                time.sleep(2)

        return task_info
    def get_handler(self):
        task_info = self.get_task()
        cookie_obj = AccountRedisInterface().get_cookie()
        task_name = task_info.get('task_name')
        task_contain =task_info.get("task_contain")
        req_info = RequestFactory.factory()[task_name](task_name,cookie_obj,task_contain)
        res =requests.post(url=req_info['url'],headers=req_info['headers'],data=req_info['body'])
        print(res.text)
        if res.status_code == 200:
            return True,task_info,res.text
        else:
            return False,task_info,None
    def run(self):
        while True:
            try:
                task_statue, task_info, response = self.get_handler()
                if task_statue:
                    logger.info(f"任务{task_info.get('task_name')} 执行完成！，完成响应：{response}")
                else:
                    # 任务回滚！
                    logger.info(f"任务{task_info.get('task_name')} 异常回滚！")
                    task_redis_client.lpush('instagram:task',task_info)
            except Exception as e:
                logger.error(e)
            time.sleep(2)



if __name__ == '__main__':
    spider = SpiderInteractive().get_task()


