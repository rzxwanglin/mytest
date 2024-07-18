import json
import time
import requests
import config
from loguru import logger
from config import task_redis_client
from config import storage_redis_client
from utilis.account_redis_interface import AccountRedisInterface
from utilis.distribution_task import DistributionTask
from request_factory import RequestFactory
class SpiderData(object):
    """
    一级爬虫任务
    """
    def __init__(self):
        logger.info('初始化instagram数据爬虫')

    def post_parse(self, task_info):
        pass


    def get_task(self):
        while True:
            task_info = task_redis_client.lpop(config.task_data)
            if task_info:
                return json.loads(task_info)
            else:
                time.sleep(2)

    def get_handler(self):
        data_dict = self.get_task()
        task_name = data_dict['task_name']
        seed = data_dict.get("seed", None)
        if task_name not in ['user']:
            cookie_obj = AccountRedisInterface().get_cookie()
            if not cookie_obj:
                return False, data_dict, None
        else:
            cookie_obj = None
        if task_name in ["liked"]:
            # todo post_id
            post_id = data_dict.get("source_post", {}).get("id")
            req_info = RequestFactory.factory()[task_name](task_name, cookie_obj, post_id)
        elif task_name in ["comment", "post", "user", "following", "follower", "hashtag", "search", "post_id"]:
            req_info = RequestFactory.factory()[task_name](task_name, cookie_obj, seed)
        else:
            return False, data_dict, None
        # todo 优化代码
        if config.use_proxy:
            proxie = config.proxies
            res =requests.request(method=req_info['method'],url=req_info['url'],headers=req_info['headers'],data=req_info.get('body',''),proxies=proxie)

        else:
            res = requests.request(method=req_info['method'], url=req_info['url'], headers=req_info['headers'],
                                   data=req_info.get('body', ''))

        if res.status_code == 200 and '"status":"ok"' in res.text:
            return True,data_dict,res.text
        else:
            logger.error("!!任务执行异常！！")
            return False,data_dict,None

    def run(self):
        while True:
            try:
                task_statue, task_info, response = self.get_handler()
                if task_statue:
                    logger.info(f"任务{task_info.get('task_name')} 执行完成！，完成响应：{response}")
                    result ={
                        'task_info':task_info,
                        'task_result':response
                    }
                    storage_redis_client.lpush(config.task_storage+task_info.get('task_name'),json.dumps(result))
                    if task_info.get('task_name') == 'user':
                        seed = ''
                        for task_ in ['follower','following','comment','liked']:
                            DistributionTask().distribute_task(task_info,task_,seed)

                else:
                    # 任务回滚！
                    logger.error(response)
                    # todo 判断是否是账号失效，如果是账号失效要redis 直接删除 instagram_cookie_total_hash 中对应多key  以及instagram_cookie_total_zest 中多key
                    logger.info(f"任务{task_info.get('task_name')} 异常回滚！")
                    task_redis_client.rpush(config.task_data, json.dumps(task_info))

            except Exception as e:
                logger.error(e)
                logger.info(f"任务{task_info.get('task_name')} 异常回滚！")
                task_redis_client.rpush(config.task_data, json.dumps(task_info))
            time.sleep(2)



if __name__ == '__main__':
    spider = SpiderInteractive().get_task()


