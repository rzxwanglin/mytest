import config
import json
import base64
import time
import datetime
from config import app
from utilis.account_redis_interface import AccountRedisInterface
from config import account_redis_client
from config import task_redis_client
from config import data_redis_client
from loguru import logger
from flask import Flask
from flask import request, Response, jsonify
from flask import render_template, url_for, redirect, send_from_directory, make_response, send_file
from rhino_v2_utilis.handler.redis_handler import CRedisHandler


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/put/account', methods=['POST'])
def put_account():
    """
        instagram:login:account:password:hash
        account_info 账号:密码:邮箱:邮箱二次验证
    """
    # 判断账号是否符合条件
    user = request.form['user']
    account_info = request.form['account_info']
    if len(account_info.split(':')) == 4:
        account_redis_client.hset('instagram:login:account:password:hash',account_info,user)
        return '添加完成！'
    else:
        return f'请检查格式:{account_info}'


@app.route('/api/get/cookie', methods=['GET'])
def get_login_cookie():
    cookie = AccountRedisInterface().get_cookie()
    print(cookie)
    return jsonify(cookie)



@app.route('/api/inter/addtask', methods=['POST'])
def inter_add_task():
    """
    task_info =
        {
            "task_name": ""   1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
            ,"task_type": ""  action ,caiji
            ,"task_status": "" add run end
            ,"task_created_date": "" 时间戳
            ,"task_created": "" tag
            ,"task_contain": {"seed":"https://ddd","text":"hello"} #seed_type :帖子 或者 作者主页
        }

        还应该将用户加入到，用户key中做持久化处理

    """
    from_user_json = request.get_json()
    task_name = from_user_json['task_name']
    user_name = from_user_json['user_name']
    task_details = from_user_json["task_details"]

    print(task_details)
    if task_name == '点赞':
        task_name = 'like_inter'
        task_type = 'inter'
    elif task_name == '评论':
        task_name = 'comment_inter'
        task_type = 'inter'
    elif task_name == '关注':
        task_name = 'click_inter'
        task_type = 'inter'
    else:
        return '请检查任务类型【点赞、关注、评论】'
    task_type = task_type
    task_status = 'run'  # end

    task_created_date = time.time()
    task_info = {
            "id":"1008611" # 随机 7位
            ,"task_name": task_name   #1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
            ,"task_type": task_type # action ,caiji
            ,"task_status": task_status #add run end
            ,"task_created_date": task_created_date #时间戳
            ,"user_name": user_name # tag
            ,"task_details":task_details # 任务细节
    }
    # todo 添加到配置表中
    task_redis_client.lpush(config.task_inter, json.dumps(task_info))
    #判断用户是否在表中
    user = json.loads(task_redis_client.hget("instagram:users",user_name))
    if user:
        use_cookie_count =user.get("use_cookie_count",0)+1
        task_count = user.get("task_count",0)+1
        task_redis_client.hset("instagram:users", user_name,json.dumps({"use_cookie_count":use_cookie_count,"task_count":task_count}))
    else:
        task_redis_client.hset("instagram:users", user_name, json.dumps({"use_cookie_count":1,"task_count":1}))
    task_redis_client.lpush(f"instagram:task:history:{user_name}", json.dumps(task_info))


    return '任务上传完毕'

@app.route('/api/data/addtask', methods=['POST'])
def data_add_task():
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
    task_info = {'task_info': {'id': '9470055', 'type': 'instagram','user':'',
                              'params': {'seed': '',
                              'seed_type': 'user',
                              'task': [],
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
                               }}
    from_user_json = request.get_json()
    task_info['task_info']['user'] = from_user_json['user']
    task_info['task_info']['params']['seed'] = from_user_json['seed']
    task_info['task_info']['params']['task'] = from_user_json["task"].split(':')
    task_redis_client.lpush(config.task_info_name, json.dumps(task_info))
    return jsonify(task_info)

@app.route('/test',methods=['POST'])
def test_post():
    request_data = request.get_json()
    print(request_data)
    return '1'

if __name__ == "__main__":
    logger.add(
        config.log_path,
        retention="3 days",
        rotation="100 MB",
        format="{message}",
        encoding="utf-8",
        enqueue=False,
    )
    app.run(host='0.0.0.0', port=5004, debug=True)
