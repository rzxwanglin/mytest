import requests
import json
from request_factory import RequestFactory
from task_spider.spider_interactive import SpiderInteractive


#
proxy ={
   'http':'http://127.0.0.1:8800',
    'https':'http://127.0.0.1:8800'
}

res = requests.get('http://127.0.0.1:5003/api/get/cookie')
print(res.json())
cookie_obj =json.loads(res.json())



task = 'like_inter'
cookie_obj['media_id'] ='3393245210130807279'
req_info= RequestFactory.make_request_like_inter(task,cookie_obj)
print(req_info)
res =requests.post(url=req_info['url'],headers=req_info['headers'],data=req_info['body'],proxies=proxy)
print(res.text)



# res = requests.get('http://127.0.0.1:5003/api/get/cookie')
# print(res.json())
# cookie_obj =json.loads(res.json())
#


task = 'comment_inter'
cookie_obj['text'] ='cool'
cookie_obj['media_id'] ='3402868696348256145'
req_info= RequestFactory.make_request_comment_inter(task,cookie_obj)
print(req_info)
res =requests.post(url=req_info['url'],headers=req_info['headers'],data=req_info['body'],proxies=proxy)
print(res.text)

task = 'click_inter'
task_contain={
    'user_id':'65862573148'
}
req_info= RequestFactory.make_request_click_inter(task,cookie_obj,task_contain)
print(req_info)
res =requests.post(url=req_info['url'], headers=req_info['headers'], data=req_info['body'])
print(res.text)