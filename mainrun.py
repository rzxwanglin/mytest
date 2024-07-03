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


@app.route('/login/put/account', methods=['POST'])
def put_account():
    """
        instagram:login:account:password:hash
        account_info 账号:密码:邮箱:邮箱二次验证
    """
    user = request.form['user']
    account_info = request.form['account_info']
    account_redis_client.hset('instagram:login:account:password:hash',account_info,user)
    return '添加完成！'

@app.route('/api/put/cookie', methods=['POST'])
def login_cookie():
    """
            拿到账号 密码 构造 user-task
            上传redis
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cookie = request.form['cookie']

    return ''

@app.route('/api/get/cookie', methods=['GET'])
def get_login_cookie():
    cookie = AccountRedisInterface().get_cookie()
    print(cookie)

    return  jsonify(cookie)


@app.route('/api/addtask', methods=['POST'])
def api_add_task():
    """
    task_info =
        {
            "task_name": ""   1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
            ,"task_type": ""  action ,caiji
            ,"task_status": "" add run end
            ,"task_created_date": "" 时间戳
            ,"task_created": "" tag
        }
    """
    task_name= request.form['task_name']
    task_type= request.form['task_type']
    task_status=request.form['task_status']
    user_name= request.form['user_name']
    task_created_date = time.time()
    task_info = {
            "task_name": task_name   #1、点赞2、评论3、关注4、发帖子5、采集帖子观看数量6、点赞数量
            ,"task_type": task_type # action ,caiji
            ,"task_status": task_status #add run end
            ,"task_created_date": task_created_date #时间戳
            ,"user_name": user_name # tag
        }
    task_redis_client.lpush(f"instagram:task:{user_name}", task_info)
    """
    将task_info 转成json
    提取对应的的信息，入库到redis
    """

    return '任务上传完毕'


if __name__ == "__main__":
    # redis_client.hset("test:redis","123","443344")
    logger.add(
        config.log_path,
        retention="3 days",
        rotation="100 MB",
        format="{message}",
        encoding="utf-8",
        enqueue=False,
    )
    app.run(host='0.0.0.0', port=5003, debug=True)
