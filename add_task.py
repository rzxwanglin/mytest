import requests

res =requests.post(url='http://127.0.0.1:5004/api/data/addtask', json={'user':'test001','seed':'leomessi','task':'user:post:following'})
print(res.text)