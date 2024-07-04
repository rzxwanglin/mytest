import requests,json


# res = requests.get('http://127.0.0.1:5003/api/get/cookie')
# print(res.json())
# print(type(res.json()))
# a = json.loads(res.json())
# print(a)
# print(type(a))
# print(a['cookie'])
"""

task_details = {}

"""
api = 'http://127.0.0.1:5003'
url =api+'/api/addtask'
data ={
    "task_name":"关注",
    "user_name":"test001",
    "task_details": '{"user_id":"65862573148"}'             # user_id 需要关注的用户id
}
res = requests.post(url =url,data=data)
print(res.text)
