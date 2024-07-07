import requests

data ={
    "seed":"kl_nagarkoti_5_",   #task_name 任务类型  目前只支持 评论、点赞、关注
    "task":['user', 'follower', 'following', 'post', 'liked', 'comment'], # 用户名称 随便填写
    "user": "test001"          # user_id 需要关注的用户id
}
res =requests.post('http://127.0.0.1:5003/api/data/addtask',json=data)
print(res.text)


task_ = {"task_name": "user", "task_type": "data", "task_status": "add", "task_created_date": 1720359363.2654562, "user_name": "test001", "task_details": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "father_task": {"task_info": {"id": "9470055", "type": "instagram", "user": "test001", "params": {"seed": ["kl_nagarkoti_5_"], "seed_type": "user", "task": ["user", "follower", "following", "post", "liked", "comment"], "limit": {"user": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "follower": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "following": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "post": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "liked": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}, "comment": {"count": 50, "crawl_image": false, "frequencyAuto": 0, "after": "2023-09-01 00:00:00 +0800"}}}}}, "seed": ["kl_nagarkoti_5_"], "seed_type": "user"}

