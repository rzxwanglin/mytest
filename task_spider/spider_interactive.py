import json
import time
import requests
import config
from loguru import logger
from config import task_redis_client
from config import storage_redis_client
from utilis.account_redis_interface import AccountRedisInterface
from request_factory import RequestFactory
class SpiderInteractive(object):
    """
    二级爬虫任务
    """
    def __init__(self):
        logger.info('初始化instagram交互爬虫')

    def get_task(self):
        while True:
            task_info = task_redis_client.lpop(config.task_inter)
            if task_info:
                break
            else:
                time.sleep(2)

        return json.loads(task_info)

    def parse_userid(self,user):
        req_info = RequestFactory.factory()['user']('user', {}, user)
        if config.use_proxy:
            proxie = config.proxies
            res = requests.request(method=req_info['method'], url=req_info['url'], headers=req_info['headers'],
                                   data=req_info.get('body', ''), proxies=proxie)

        else:
            res = requests.request(method=req_info['method'], url=req_info['url'], headers=req_info['headers'],
                                   data=req_info.get('body', ''))
        try:
             userid= res.json()['user']['id']
        except:
            userid =None
        return userid
    def parse_media_id(self,cookie_obj,media_id):
        req_info = RequestFactory.factory()['post_id']('post_id', cookie_obj, media_id)
        if config.use_proxy:
            proxie = config.proxies
            res = requests.request(method=req_info['method'], url=req_info['url'], headers=req_info['headers'],
                                   data=req_info.get('body', ''), proxies=proxie)

        else:
            res = requests.request(method=req_info['method'], url=req_info['url'], headers=req_info['headers'],
                                   data=req_info.get('body', ''))
        try:
            media_id = res.json()['data']['xdt_shortcode_media']['id']
        except:
            media_id = None
        return media_id

    def get_handler(self):
        task_info = self.get_task()
        cookie_obj = AccountRedisInterface().get_cookie()
        if not cookie_obj:
            return False, task_info, None
        task_name = task_info.get('task_name')
        task_contain =task_info.get("task_details")
        if task_name=='click_inter':
            if not isinstance(task_contain, dict):
                task_contain = json.loads(task_contain)
            task_contain['user_id'] = self.parse_userid(task_contain['media_id'])
        else:
            if not isinstance(task_contain, dict):
                task_contain = json.loads(task_contain)
            task_contain['media_id'] = self.parse_media_id(cookie_obj,task_contain['media_id'])

        req_info = RequestFactory.factory()[task_name](task_name,cookie_obj,task_contain)
        # todo 优化代码
        if config.use_proxy:
            proxie = config.proxies
            res =requests.post(url=req_info['url'],headers=req_info['headers'],data=req_info['body'],proxies=proxie)
        else:
            res = requests.post(url=req_info['url'], headers=req_info['headers'], data=req_info['body'])
        if res.status_code == 200 and '"status":"ok"' in res.text and 'execution error' not in res.text:
            return True,task_info,res.text
        else:
            logger.error("!!任务执行异常！！")
            return False,task_info,None

    def run(self):
        while True:
            try:
                task_statue, task_info, response = self.get_handler()
                if task_statue:
                    logger.info(f"任务{task_info.get('task_name')} 执行完成！，完成响应：{response}")
                    result = {
                        'task_info': task_info,
                        'task_result': response
                    }
                    storage_redis_client.rpush(config.task_storage + task_info.get('task_name'), json.dumps(result))
                else:
                    # 任务回滚！
                    # todo 判断是否是账号失效，如果是账号失效要redis 直接删除 instagram_cookie_total_hash 中对应多key  以及instagram_cookie_total_zest 中多key
                    logger.info(f"任务{task_info.get('task_name')} 异常回滚！")
                    task_redis_client.rpush(config.task_inter, json.dumps(task_info))

            except Exception as e:
                logger.error(e)
            time.sleep(2)



if __name__ == '__main__':
    spider = SpiderInteractive().get_task()


