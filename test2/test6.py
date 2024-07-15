from websocket import WebSocketApp
import base64
import execjs,time
import re,ssl
try:
    import thread
except ImportError:
    import _thread as thread
import websocket


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


    def send1(self):
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
        print(result)
        binary_data = base64.b64decode(result['code'])
        return binary_data
    def send2(self,message):
        with open('data/my.js', 'r', encoding='utf-8') as file:
            js = file.read()

        # 使用execjs编译JavaScript代码
        ctx = execjs.compile(js)
        # 执行JavaScript函数
        result = ctx.call("get_mycode2", message)
        print(result)
        binary_data = base64.b64decode(result['code'])
        return binary_data

    def on_open(self, ws):
        print("####### on_open #######")
        binary_data = self.send1()
        print(binary_data)
        # 确保二进制数据有效
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217082445666103582,\"tasks\":[{\"failure_count\":null,\"label\":\"207\",\"payload\":\"{\\\"contact_id\\\":17846712582227458}\",\"queue_name\":\"cpq_v2\",\"task_id\":0},{\"failure_count\":null,\"label\":\"207\",\"payload\":\"{\\\"contact_id\\\":17847541137225015}\",\"queue_name\":\"cpq_v2\",\"task_id\":1},{\"failure_count\":null,\"label\":\"207\",\"payload\":\"{\\\"contact_id\\\":17843216595237645}\",\"queue_name\":\"cpq_v2\",\"task_id\":2}],\"version_id\":\"7816272465125243\"}","request_id":4,"type":3}'
        binary_data = self.send2(message)
        print(binary_data)
        # 确保二进制数据有效
        self.ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        time.sleep(1)
        message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217073016432346726,\"tasks\":[{\"failure_count\":null,\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"otid\\\":\\\"7217072965740846377\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"sync_group\\\":1,\\\"mark_thread_read\\\":1,\\\"text\\\":\\\"cccc123\\\",\\\"initiating_source\\\":1,\\\"skip_url_preview_gen\\\":0,\\\"text_has_links\\\":0,\\\"multitab_env\\\":0}\",\"queue_name\":\"17846712582227458\",\"task_id\":12},{\"failure_count\":null,\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"last_read_watermark_ts\\\":1720684281764,\\\"sync_group\\\":1}\",\"queue_name\":\"17846712582227458\",\"task_id\":13}],\"version_id\":\"7816272465125243\",\"data_trace_id\":\"#mh1JDp0wS92uyj5oTkGKJw\"}","request_id":31,"type":3}'
        binary_data = self.send2(message)
        print(binary_data)
        # 确保二进制数据有效
        self.ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        
    def run(self, *args):
        while True:
            time.sleep(1)
            input_msg = input("输入要发送的消息（ps：输入关键词 close 结束程序）:\n")
            if input_msg == "close":
                self.ws.close()  # 关闭
                print("thread terminating...")
                break
            else:
                self.ws.send(input_msg)




    def start(self):
        websocket.enableTrace(True)  # 开启运行状态追踪。debug 的时候最好打开他，便于追踪定位问题。
        headers= [
            'Pragma: no-cache',
            'Cache-Control: no-cache',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Encoding: gzip, deflate, br, zstd',
            'Accept-Language: zh-CN,zh;q=0.9',
            'Sec-WebSocket-Extensions: client_max_window_bits',
            #'Cookie:ig_did=76DFB32F-D234-4309-88AA-E6085C5374C6; datr=7T9pZoYHevj9WSFhe-s9Lhsz; mid=Zmk_8gALAAEQ4k_rOLpfRB5FrTG4; ig_nrcb=1; csrftoken=FZGIoEaEpeQCbe0cj6tEmMkGpm6wIQWN; ds_user_id=66898393014; shbid="12767\05466898393014\0541751946935:01f7175bf8b59f18c60dad0fac890a2d709f8f8b42efc61f1563365e846b0cbac58ce794"; shbts="1720410935\05466898393014\0541751946935:01f7133519b38846542e1627147181f396a73dd6449a087890f5541d26d279b842055d6a"; ps_n=1; ps_l=1; wd=861x755; sessionid=66898393014%3AY2FdkTsrtNzsOj%3A0%3AAYf9W9qm9g_L8OeGOT0QwriUjfBGuxOMJipuDCZKe5U; rur="CCO\05466898393014\0541752205853:01f705ffdc24e60d87b0cfe1961ec725723f964f49eb217249511477d3d7ea7ec857d238"'
        ]
        self.ws = WebSocketApp(self.url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_close=self.on_close,
                               cookie='ig_did=76DFB32F-D234-4309-88AA-E6085C5374C6; datr=7T9pZoYHevj9WSFhe-s9Lhsz; mid=Zmk_8gALAAEQ4k_rOLpfRB5FrTG4; ig_nrcb=1; csrftoken=FZGIoEaEpeQCbe0cj6tEmMkGpm6wIQWN; ds_user_id=66898393014; ps_n=1; ps_l=1; sessionid=66898393014%3AY2FdkTsrtNzsOj%3A0%3AAYf9W9qm9g_L8OeGOT0QwriUjfBGuxOMJipuDCZKe5U; shbid="12767\05466898393014\0541752206145:01f7f20c08ab4e25342e4413f47bed0c9078e2c240169a1ab921b6d407c84f53a9de608c"; shbts="1720670145\05466898393014\0541752206145:01f7506663d9e1acd2da92eb376456471bf3dcfbe3e53d0af4dc4da868ac362f07dfe708"; wd=1325x755; rur="CCO\05466898393014\0541752219978:01f744264737b47c00b522fa4ee059409b62edad711077e0e52c268d11a936d4a51c9642"'

                               ,header=headers
                               )
        self.ws.run_forever(http_proxy_host="127.0.0.1", http_proxy_port=10900, proxy_type='http',sslopt={"cert_reqs": ssl.CERT_NONE})



if __name__ == '__main__':
    with open('data/ini.txt', 'r', encoding='utf-8') as f:
        url = f.read()

    Test(url).start()


