import requests,json


api = 'http://127.0.0.1:5004'


url =api+'/api/inter/addtask'

data ={
    "task_name":"关注",   #task_name 任务类型  目前只支持 评论、点赞、关注
    "user_name":"test001", # 用户名称 随便填写
    "task_details": {"user_id":"01mustafacot"}             # user_id 需要关注的用户id
}
res = requests.post(url =url,json=data)
print(res.text)


data ={
    "task_name":"评论",   #task_name 任务类型  目前只支持 评论、点赞、关注
    "user_name":"test001", # 用户名称 随便填写
    "task_details": {"text":"cool","media_id":"CdNQHA8uyRi"}             # media_id需要评论到 帖子id  text 需要评论到内容
}
res = requests.post(url =url,json=data)
print(res.text)


data ={
    "task_name":"点赞",   #task_name 任务类型  目前只支持 评论、点赞、关注
    "user_name":"test001", # 用户名称 随便填写
    "task_details": {"media_id":"CdNQHA8uyRi"}             # media_id 需要点赞到帖子id
}
res = requests.post(url =url,json=data)
print(res.text)



