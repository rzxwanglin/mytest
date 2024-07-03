import requests,json


res = requests.get('http://127.0.0.1:5003/api/get/cookie')
print(res.json())
print(type(res.json()))
a = json.loads(res.json())
print(a)
print(type(a))
print(a['cookie'])