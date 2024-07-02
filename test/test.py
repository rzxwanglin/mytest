import requests


res = requests.get('http://127.0.0.1:5003/api/get/cookie')
print(res.text)