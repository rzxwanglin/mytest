import copy
import logging
import time
import config
import json
from config import task_redis_client
class DistributionTask:
    """
    {'task_info': {'id': '9470055', 'type': 'instagram','user':'test001',
                   'params': {'seed': ['kl_nagarkoti_5_'],
                              'seed_type': 'user',
                              'task': ['user', 'follower', 'following', 'post', 'liked', 'comment'],
                              'limit': {
                                       'user': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                'after': '2023-09-01 00:00:00 +0800'},
                                       'follower': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                    'after': '2023-09-01 00:00:00 +0800'},
                                       'following': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                     'after': '2023-09-01 00:00:00 +0800'},
                                       'post': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                'after': '2023-09-01 00:00:00 +0800'},
                                       'liked': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                 'after': '2023-09-01 00:00:00 +0800'},
                                       'comment': {'count': 50, 'crawl_image': False, 'frequencyAuto': 0,
                                                   'after': '2023-09-01 00:00:00 +0800'}
                                            }
                                        }
                        }
    """
    def __init__(self):
        self.client = task_redis_client

    def distribute_task(self,task_infos,task_,seed):
        if isinstance(task_infos, str):
            task_infos = json.loads(task_infos)
        if task_infos:
            user_name = task_infos['user_name']
            params = task_infos['father_task']['task_info']['params']
            seed_ = params['seed']
            tasks = params['task']
            limit = params['limit']
            task_created_date = time.time()
            task_info = {
                "task_id": task_infos['task_id'],
                "task_name": task_  # 1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
                , "task_type": "data"  # action ,caiji
                , "task_status": "add"  # add run end
                , "task_created_date": task_created_date  # 时间戳
                , "user_name": user_name  # tag
                , "task_details": limit[task_]  # 任务细节
                , "father_task": copy.deepcopy(task_infos)
                , "seed": seed
                , "seed_": seed_
                , "seed_type": params['seed_type']
            }
            logging.error(f"拆分二级任务{task_} 完成")
            task_redis_client.lpush(config.task_data, json.dumps(task_info))
            # 判断用户是否在表中
            user = task_redis_client.hget("instagram:users", user_name)
            if user:
                user = json.loads(user)
                use_cookie_count = user.get("use_cookie_count", 0) + 1
                task_count = user.get("task_count", 0) + 1
                task_redis_client.hset("instagram:users", user_name,
                                       json.dumps(
                                           {"use_cookie_count": use_cookie_count, "task_count": task_count}))
            else:
                task_redis_client.hset("instagram:users", user_name,
                                       json.dumps({"use_cookie_count": 1, "task_count": 1}))

            task_redis_client.lpush(f"instagram:task:history:{user_name}", json.dumps(task_info))

            try:
                # 生成二级任务 task_data = instagram:data:task
                pass
            except:
                # todo 记录异常任务
                logging.error('任务拆分异常！')
            time.sleep(1)

    # def distribute(self, task_infos,seed):
    #
    #     task_infos = self.client.lpop(config.task_info_name)


    def run(self):
        while True:
            task_infos = self.client.lpop(config.task_info_name)
            if isinstance(task_infos, str):
                task_infos = json.loads(task_infos)
            if task_infos:
                user_name = task_infos['task_info']['user']
                params = task_infos['task_info']['params']
                seed = params['seed']
                tasks = params['task']
                limit = params['limit']
                for task in tasks:
                    if task == '' or task in ['follower', 'following', 'comment', 'liked']:
                        continue
                    task_created_date = time.time()
                    task_info = {
                        "task_id": task_infos['task_info']['id'],
                        "task_name": task  # 1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
                        , "task_type": "data"  # action ,caiji
                        , "task_status": "add"  # add run end
                        , "task_created_date": task_created_date  # 时间戳
                        , "user_name": user_name  # tag
                        , "task_details": limit[task]  # 任务细节
                        , "father_task": copy.deepcopy(task_infos)
                        , "seed": seed
                        , "seed_type": params['seed_type']
                    }
                    logging.error(f"拆分二级任务{task} 完成")
                    task_redis_client.lpush(config.task_data, json.dumps(task_info))
                    # 判断用户是否在表中
                    user = task_redis_client.hget("instagram:users", user_name)
                    if user:
                        user = json.loads(user)
                        use_cookie_count = user.get("use_cookie_count", 0) + 1
                        task_count = user.get("task_count", 0) + 1
                        task_redis_client.hset("instagram:users", user_name,
                                               json.dumps(
                                                   {"use_cookie_count": use_cookie_count, "task_count": task_count}))
                    else:
                        task_redis_client.hset("instagram:users", user_name,json.dumps({"use_cookie_count": 1, "task_count": 1}))

                    task_redis_client.lpush(f"instagram:task:history:{user_name}", json.dumps(task_info))
                try:
                    # 生成二级任务 task_data = instagram:data:task
                    pass
                except:
                    # todo 记录异常任务
                    logging.error('任务拆分异常！')
                time.sleep(1)


