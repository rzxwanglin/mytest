# 文档内容
该文档介绍了如何使用一个提供任务添加功能的API。

该API的基础URL为 http://127.0.0.1:5003。（等待部署到服务器）


导入必要的库

```python
import requests
import json
```

接口地址


```python
api = 'http://127.0.0.1:5003'
```
## 添加关注任务

**URL:** /api/addtask

**请求方式:** POST

**请求参数:**
- `task_name` (str): 任务类型，当前支持 `评论`、`点赞`、`关注`
- `user_name` (str): 用户名称，可以随意填写
- `task_details` (json): 任务详细信息，这里包含需要关注的用户ID

**示例代码:**

```python
url = api + '/api/addtask'
data = {
    "task_name": "关注",   # 任务类型 目前只支持 评论、点赞、关注
    "user_name": "test001", # 用户名称 随便填写
    "task_details": json.dumps({"user_id": "65862573148"})  # user_id 需要关注的用户id
}
res = requests.post(url=url, data=data)
print(res.text)
```
## 添加评论任务

**URL:** /api/addtask

**请求方式:** POST

**请求参数:**
- `task_name` (str): 任务类型，当前支持 `评论`、`点赞`、`关注`
- `user_name` (str): 用户名称，可以随意填写
- `task_details` (json): 任务详细信息，这里包含需要评论的内容和帖子ID

**示例代码:**

```python
url = api + '/api/addtask'
data = {
    "task_name": "评论",   # 任务类型 目前只支持 评论、点赞、关注
    "user_name": "test001", # 用户名称 随便填写
    "task_details": json.dumps({"text": "cool", "media_id": "3402868696348256145"})  # media_id需要评论到 帖子id, text 需要评论到内容
}
res = requests.post(url=url, data=data)
print(res.text)
```
## 添加点赞任务

**URL:** /api/addtask

**请求方式:** POST

**请求参数:**
- `task_name` (str): 任务类型，当前支持 `评论`、`点赞`、`关注`
- `user_name` (str): 用户名称，可以随意填写
- `task_details` (json): 任务详细信息，这里包含需要点赞的帖子ID

**示例代码:**

```python
url = api + '/api/addtask'
data = {
    "task_name": "点赞",   # 任务类型 目前只支持 评论、点赞、关注
    "user_name": "test001", # 用户名称 随便填写
    "task_details": json.dumps({"media_id": "3393245210130807279"})  # media_id 需要点赞到帖子id
}
res = requests.post(url=url, data=data)
print(res.text)
```
