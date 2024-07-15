import execjs,base64
import time
import websocket
import re
with open('data/ini.txt','r+',encoding='utf-8') as f:
    url = f.read()
pat1 =re.compile('sid=(.*?)&cid')
sid = re.findall(pat1,url)[0]
cid =url.split('cid=')[1]


with open('data/opensend.js','r+',encoding='utf-8') as file:
    js =file.read()




# 使用execjs编译JavaScript代码
ctx = execjs.compile(js)
# 执行JavaScript函数
result = ctx.call("get_mycode",cid,sid)
print(type(result))
print(result)  # 输出: Hello, World!
binary_data = base64.b64decode(result['code'])
print(binary_data)

headers = [
    'Pragma: no-cache',
    'Cache-Control: no-cache',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding: gzip, deflate, br, zstd',
    'Accept-Language: zh-CN,zh;q=0.9',
    'Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits',
    'Cookie:mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYe0vCvaB8YWCPy2npkAWzYvIq3B9SwU6kssbshNcS0; shbid="3441\05466881971457\0541752199519:01f7d019e08e168da954c6143ba03d34cc3ecffd2b5baa865c21e2dd9ab2eccbdd5cdc2b"; shbts="1720663519\05466881971457\0541752199519:01f7796ec0c5745502b04592bcbd1b48ebad4954ac39f034c3f35f8bef0fcc7daac8e3c5"; wd=500x623; rur="CCO\05466881971457\0541752212774:01f7478507535d55fae3997d0770ba18d9b7ab2fe5db33049c2314a3a8d56855d8fb60e6"'
]

try:
    ws = websocket.create_connection(url, header=headers,http_proxy_host='172.17.32.1',http_proxy_port=9000)
    print("WebSocket connection established")
    ws.send(binary_data)
    print("Sent a message")
    # Example of receiving a message
    while True:
        try:
            response = ws.recv()
            print(type(response))
            print(len(response))
            print("Received a message: ", response)
            time.sleep(1)
            ws.send(binary_data)
            print("Sent a message")
        except Exception as e:
            print(e)
            time.sleep(1)

    ws.close()
except websocket.WebSocketBadStatusException as e:
    print(f"Failed to establish WebSocket connection: {e}")
except Exception as e:
    print(f"An error occurred: {e}")



