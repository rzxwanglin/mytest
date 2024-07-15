# -*- coding:utf-8 -*-

"""
@author:    tz_zs
"""

import websocket
from websocket import WebSocketApp

try:
    import thread
except ImportError:
    import _thread as thread
import time
import execjs, base64
import re


class Test(object):
    def __init__(self, url):
        super(Test, self).__init__()
        self.url = url
        self.ws = None

    def on_message(self, ws, message):
        print("####### on_message #######")
        print("message：%s" % message)



    def on_close(self, ws, close_status_code, close_msg):
        print("####### on_close #######")
        print(f"close_status_code: {close_status_code}")
        print(f"close_msg: {close_msg}")


    def on_open(self, ws):
        print("####### on_open #######")
        with open('data/ini.txt', 'r', encoding='utf-8') as f:
            url = f.read()
        pat1 = re.compile('sid=(.*?)&cid')
        sid = re.findall(pat1, url)[0]
        cid = url.split('cid=')[1]
        with open('data/opensend.js', 'r', encoding='utf-8') as file:
            js = file.read()
        # 使用execjs编译JavaScript代码
        ctx = execjs.compile(js)
        # 执行JavaScript函数
        result = ctx.call("get_mycode", cid, sid)
        print(type(result))
        print(result)  # 输出: Hello, World!
        binary_data = bytes(base64.b64decode(result['code']))
        print(binary_data)
        print(type(binary_data))
        self.ws.send(binary_data, binary=True)

    def start(self):
        websocket.enableTrace(True)  # 开启运行状态追踪。debug 的时候最好打开他，便于追踪定位问题。

        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_close=self.on_close,
                               cookie='mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYe0vCvaB8YWCPy2npkAWzYvIq3B9SwU6kssbshNcS0; shbid="3441\05466881971457\0541752199519:01f7d019e08e168da954c6143ba03d34cc3ecffd2b5baa865c21e2dd9ab2eccbdd5cdc2b"; shbts="1720663519\05466881971457\0541752199519:01f7796ec0c5745502b04592bcbd1b48ebad4954ac39f034c3f35f8bef0fcc7daac8e3c5"; wd=500x623; rur="CCO\05466881971457\0541752212774:01f7478507535d55fae3997d0770ba18d9b7ab2fe5db33049c2314a3a8d56855d8fb60e6"'
                               )

        # self.ws.on_open = self.on_open  # 也可以先创建对象再这样指定回调函数。run_forever 之前指定回调函数即可。

        self.ws.run_forever(http_proxy_host="172.17.32.1", http_proxy_port=9000, proxy_type='http')
        # self.ws.run_forever(http_proxy_host="192.168.1.110", http_proxy_port=1080, proxy_type='socks5')

if __name__ == '__main__':
    with open('data/ini.txt', 'r', encoding='utf-8') as f:
        url = f.read()

    Test(url).start()


