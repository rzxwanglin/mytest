import json

from websocket import WebSocketApp
import base64
import execjs,time,ssl
import re,requests,math,random
try:
    import thread
except ImportError:
    import _thread as thread
import websocket


class Test(object):
    def __init__(self,cid,aid):
        super(Test, self).__init__()
        self.sid = math.floor(random.random() * 9007199254740991)
        url = 'wss://edge-chat.instagram.com/chat?sid='+str(self.sid)+'=' + cid
        self.cid =cid
        self.aid =aid
        self.url = url
        self.ws = None

    def on_message(self, ws, message):
        print("####### on_message #######")
        print("message：%s" % message)

        with open('data/dcode.js', 'r', encoding='utf-8') as file:
            js = file.read()
        # 使用execjs编译JavaScript代码
        ctx = execjs.compile(js)
        # 执行JavaScript函数
        username = ctx.call("decodeByteMessages", list(message))
        print('!!!!!!')
        print(username)
        print('!!!!!!')

    def on_close(self, ws, close_status_code, close_msg):
        print("####### on_close #######")
        print(f"close_status_code: {close_status_code}")
        print(f"close_msg: {close_msg}")

    def send0(self):
        with open('data/all.js', 'r', encoding='utf-8') as file:
            js = file.read()
        # 使用execjs编译JavaScript代码
        ctx = execjs.compile(js)
        # 执行JavaScript函数
        username = ctx.call("get_g", self.cid,self.aid, self.sid)
        print(username)
        result = ctx.call("get_mycode", username)
        print(result)
        binary_data = base64.b64decode(result['code'])
        return binary_data

    def send2(self,req='',message='',mode=4):
        with open('data/my.js', 'r', encoding='utf-8') as file:
            js = file.read()
        # 使用execjs编译JavaScript代码
        ctx = execjs.compile(js)
        # 执行JavaScript函数
        if mode==2:
            result = ctx.call("get_mycode2", req,message)
        elif mode ==3:
            result = ctx.call("get_mycode3",req,message)
        print(result)
        binary_data = base64.b64decode(result['code'])
        return binary_data

    def on_open(self, ws):
        print("####### on_open #######")
        binary_data = self.send0()
        print(binary_data)
        # 确保二进制数据有效
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        #  "/ls_app_settings" '/ls_req' {"ls_fdid":"","ls_sv":"27033104182955117"}

        message = '{"ls_fdid":"","ls_sv":"27033104182955117"}'
        binary_data = self.send2("/ls_app_settings",message,2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        binary_data = self.send2("/ls_foreground_state", 2, 3)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        binary_data = self.send2("/ls_resp", 3, 3)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7217863283227568710,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17846712582227458}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":0},{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17847541137225015}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":1},{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17843216595237645}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":2}],\\"version_id\\":\\"8255578237827838\\"}","request_id":4,"type":3}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7217863283249807716,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"145\\",\\"payload\\":\\"{\\\\\\"is_after\\\\\\":0,\\\\\\"parent_thread_key\\\\\\":-1,\\\\\\"reference_thread_key\\\\\\":0,\\\\\\"reference_activity_timestamp\\\\\\":9999999999999,\\\\\\"additional_pages_to_fetch\\\\\\":0,\\\\\\"cursor\\\\\\":\\\\\\"HCwRAAAWnAQWiIOKjA0TBRbu1MnZz4-0PwA\\\\\\",\\\\\\"messaging_tag\\\\\\":null,\\\\\\"sync_group\\\\\\":1}\\",\\"queue_name\\":\\"trq\\",\\"task_id\\":3},{\\"failure_count\\":null,\\"label\\":\\"145\\",\\"payload\\":\\"{\\\\\\"is_after\\\\\\":0,\\\\\\"parent_thread_key\\\\\\":-1,\\\\\\"reference_thread_key\\\\\\":0,\\\\\\"reference_activity_timestamp\\\\\\":9999999999999,\\\\\\"additional_pages_to_fetch\\\\\\":0,\\\\\\"cursor\\\\\\":null,\\\\\\"messaging_tag\\\\\\":null,\\\\\\"sync_group\\\\\\":95}\\",\\"queue_name\\":\\"trq\\",\\"task_id\\":4}],\\"version_id\\":\\"8255578237827838\\"}","request_id":5,"type":3}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"database\\":1,\\"epoch_id\\":7217863283266474529,\\"failure_count\\":null,\\"last_applied_cursor\\":\\"HCwRAAAWnAQWiIOKjA0TBRbu1MnZz4-0PwA\\",\\"sync_params\\":null,\\"version\\":8255578237827838}","request_id":6,"type":2}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"database\\":2,\\"epoch_id\\":7217863283271770598,\\"failure_count\\":null,\\"last_applied_cursor\\":null,\\"sync_params\\":\\"{\\\\\\"locale\\\\\\":\\\\\\"zh_CN\\\\\\"}\\",\\"version\\":8255578237827838}","request_id":7,"type":1}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"database\\":6,\\"epoch_id\\":7217863283274037483,\\"failure_count\\":null,\\"last_applied_cursor\\":null,\\"sync_params\\":\\"{\\\\\\"locale\\\\\\":\\\\\\"zh_CN\\\\\\"}\\",\\"version\\":8255578237827838}","request_id":8,"type":1}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"database\\":7,\\"epoch_id\\":7217863283283259757,\\"failure_count\\":null,\\"last_applied_cursor\\":null,\\"sync_params\\":\\"{\\\\\\"mnet_rank_types\\\\\\":[44]}\\",\\"version\\":8255578237827838}","request_id":9,"type":1}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)

        message ='{"app_id":"936619743392459","payload":"{\\"database\\":16,\\"epoch_id\\":7217863283292568828,\\"failure_count\\":null,\\"last_applied_cursor\\":null,\\"sync_params\\":\\"{\\\\\\"locale\\\\\\":\\\\\\"zh_CN\\\\\\"}\\",\\"version\\":8255578237827838}","request_id":10,"type":1}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        message='{"app_id":"936619743392459","payload":"{\\"database\\":198,\\"epoch_id\\":7217863283301042103,\\"failure_count\\":null,\\"last_applied_cursor\\":null,\\"sync_params\\":\\"{\\\\\\"locale\\\\\\":\\\\\\"zh_CN\\\\\\"}\\",\\"version\\":8255578237827838}","request_id":11,"type":1}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        message ='{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7217863283492111140,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"123\\",\\"payload\\":\\"{\\\\\\"app_state\\\\\\":1,\\\\\\"request_id\\\\\\":\\\\\\"078e2910-2c3a-45b6-a382-8439629670cb\\\\\\"}\\",\\"queue_name\\":\\"ls_presence_report_app_state\\",\\"task_id\\":5}],\\"version_id\\":\\"8255578237827838\\"}","request_id":12,"type":3}'
        binary_data = self.send2("/ls_req", message, 2)
        print(binary_data)
        ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
        if 1==1:
            time.sleep(5)
            #发消息
            # /ls_req   {"app_id":"936619743392459","payload":"{\"label\":\"3\",\"payload\":\"{\\\"thread_key\\\":17846712582227458,\\\"is_group_thread\\\":0,\\\"is_typing\\\":0,\\\"attribution\\\":0}\",\"version\":\"8255578237827838\"}","request_id":24,"type":4}
            message = '{"app_id":"936619743392459","payload":"{\"label\":\"3\",\"payload\":\"{\\\"thread_key\\\":17846712582227458,\\\"is_group_thread\\\":0,\\\"is_typing\\\":0,\\\"attribution\\\":0}\",\"version\":\"8255578237827838\"}","request_id":24,"type":4}'
            binary_data = self.send2("/ls_req", message, 2)
            print(binary_data)
            ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
            message = '{"app_id":"936619743392459","payload":"{\"epoch_id\":7217907574699460075,\"tasks\":[{\"failure_count\":null,\"label\":\"123\",\"payload\":\"{\\\"app_state\\\":1,\\\"request_id\\\":\\\"807416cc-cff5-4ec6-89b1-766d04fdd73a\\\"}\",\"queue_name\":\"ls_presence_report_app_state\",\"task_id\":8}],\"version_id\":\"8255578237827838\"}","request_id":25,"type":3}'
            # /ls_req   {"app_id":"936619743392459","payload":"{\"epoch_id\":7217907574699460075,\"tasks\":[{\"failure_count\":null,\"label\":\"123\",\"payload\":\"{\\\"app_state\\\":1,\\\"request_id\\\":\\\"807416cc-cff5-4ec6-89b1-766d04fdd73a\\\"}\",\"queue_name\":\"ls_presence_report_app_state\",\"task_id\":8}],\"version_id\":\"8255578237827838\"}","request_id":25,"type":3}
            binary_data = self.send2("/ls_req", message, 2)
            print(binary_data)
            ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
            message ='{"app_id":"936619743392459","payload":"{\"epoch_id\":7217907690805140551,\"tasks\":[{\"failure_count\":null,\"label\":\"46\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"otid\\\":\\\"7217907574489568595\\\",\\\"source\\\":65537,\\\"send_type\\\":1,\\\"sync_group\\\":1,\\\"mark_thread_read\\\":1,\\\"text\\\":\\\"999wwww\\\",\\\"initiating_source\\\":1,\\\"skip_url_preview_gen\\\":0,\\\"text_has_links\\\":0,\\\"multitab_env\\\":0}\",\"queue_name\":\"17846712582227458\",\"task_id\":9},{\"failure_count\":null,\"label\":\"21\",\"payload\":\"{\\\"thread_id\\\":17846712582227458,\\\"last_read_watermark_ts\\\":1720883267996,\\\"sync_group\\\":1}\",\"queue_name\":\"17846712582227458\",\"task_id\":10}],\"version_id\":\"8255578237827838\",\"data_trace_id\":\"#u7x7hvzpQ0ezCkv1Onvp4g\"}","request_id":26,"type":3}'
            # /ls_req
            binary_data = self.send2("/ls_req", message, 2)
            print(binary_data)
            ws.send(binary_data, opcode=websocket.ABNF.OPCODE_BINARY)
            #'{"app_id":"936619743392459","payload":"{\\"label\\":\\"3\\",\\"payload\\":\\"{\\\\\\"thread_key\\\\\\":17846712582227458,\\\\\\"is_group_thread\\\\\\":0,\\\\\\"is_typing\\\\\\":0,\\\\\\"attribution\\\\\\":0}\\",\\"version\\":\\"8255578237827838\\"}","request_id":80,"type":4}'



            #'{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7217863283227568710,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17846712582227458}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":0},{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17847541137225015}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":1},{\\"failure_count\\":null,\\"label\\":\\"207\\",\\"payload\\":\\"{\\\\\\"contact_id\\\\\\":17843216595237645}\\",\\"queue_name\\":\\"cpq_v2\\",\\"task_id\\":2}],\\"version_id\\":\\"8255578237827838\\"}","request_id":4,"type":3}'
            #'{"app_id":"936619743392459","payload":"{\\"epoch_id\\":7217751530934351190,\\"tasks\\":[{\\"failure_count\\":null,\\"label\\":\\"145\\",\\"payload\\":\\"{\\\\\\"is_after\\\\\\":0,\\\\\\"parent_thread_key\\\\\\":-1,\\\\\\"reference_thread_key\\\\\\":0,\\\\\\"reference_activity_timestamp\\\\\\":9999999999999,\\\\\\"additional_pages_to_fetch\\\\\\":0,\\\\\\"cursor\\\\\\":\\\\\\"HCwRAAAWhgQW1oPdugcTBRbu1MnZz4-0PwA\\\\\\",\\\\\\"messaging_tag\\\\\\":null,\\\\\\"sync_group\\\\\\":1}\\",\\"queue_name\\":\\"trq\\",\\"task_id\\":3},{\\"failure_count\\":null,\\"label\\":\\"145\\",\\"payload\\":\\"{\\\\\\"is_after\\\\\\":0,\\\\\\"parent_thread_key\\\\\\":-1,\\\\\\"reference_thread_key\\\\\\":0,\\\\\\"reference_activity_timestamp\\\\\\":9999999999999,\\\\\\"additional_pages_to_fetch\\\\\\":0,\\\\\\"cursor\\\\\\":null,\\\\\\"messaging_tag\\\\\\":null,\\\\\\"sync_group\\\\\\":95}\\",\\"queue_name\\":\\"trq\\",\\"task_id\\":4}],\\"version_id\\":\\"7787689884644007\\"}","request_id":5,"type":3}'
            # 256 "{"app_id":"936619743392459","payload":"{\"database\":1,\"epoch_id\":7217751530948153847,\"failure_count\":null,\"last_applied_cursor\":\"HCwRAAAWhgQW1oPdugcTBRbu1MnZz4-0PwA\",\"sync_params\":null,\"version\":7787689884644007}","request_id":6,"type":2}"
            # 260 "{"app_id":"936619743392459","payload":"{\"database\":2,\"epoch_id\":7217751530947857387,\"failure_count\":null,\"last_applied_cursor\":null,\"sync_params\":\"{\\\"locale\\\":\\\"zh_CN\\\"}\",\"version\":7787689884644007}","request_id":7,"type":1}"
            # 260" {"app_id":"936619743392459","payload":"{\"database\":7,\"epoch_id\":7217751530952082692,\"failure_count\":null,\"last_applied_cursor\":null,\"sync_params\":\"{\\\"mnet_rank_types\\\":[44]}\",\"version\":7787689884644007}","request_id":9,"type":1}"


        # messageType:8
        # qos:0
        # topic:"/ls_foreground_state"
        # 3 ,27


        # messageIdentifier"1
        # messageType : 3
        # payloadMessage :  a {payloadString: '{"ls_fdid":"","ls_sv":"27033104182955117"}', payloadBytes: Uint8Array(42)}
        # topic: "/ls_app_settings"
        #qos:1
        #retained:false
        #64


    def start(self,cookie):
        #websocket.enableTrace(True)  # 开启运行状态追踪。debug 的时候最好打开他，便于追踪定位问题。
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
                               #cookie=cookie
                               # cookie= "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; shbid=\"3441\\05466881971457\\0541752199519:01f7d019e08e168da954c6143ba03d34cc3ecffd2b5baa865c21e2dd9ab2eccbdd5cdc2b\"; shbts=\"1720663519\\05466881971457\\0541752199519:01f7796ec0c5745502b04592bcbd1b48ebad4954ac39f034c3f35f8bef0fcc7daac8e3c5\"; wd=500x623; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYct4H0dB25022pPB7ntP0WeWDsulAfT9uwx_1R2dZM; rur=\"CCO\\05466881971457\\0541752292068:01f7cd0393c56f2ed6ceb6b4f0b1c86b2690dad06d8462b91c76400bb92b7149833b760f\""
                               cookie='mid=Zm-y1QAEAAGNHxST8H_JCHVykV7y; ig_did=A01806A7-2C0F-4928-970B-AE15EDAEEEA4; datr=1bJvZiOGH4ZJ2JnkCP17Q98E; ig_nrcb=1; csrftoken=8VKp1SN7fULQ1hBTkwmbI4VyoqNKqLrw; ds_user_id=66898393014; shbid="12767\05466898393014\0541752381644:01f7e73376330e907038d58beb2314bf7a4f1c2a38eb60346c4e0ba08e23eb2cb9907b79"; shbts="1720845644\05466898393014\0541752381644:01f7341b07e5352d70e5b797e356a12cc97f56c1680b2f96166b98856efe5a0f024c8916"; ps_n=1; ps_l=1; wd=1440x715; sessionid=66898393014%3AFx8xgxv6d0EQn3%3A26%3AAYfmmuh6dVAbkc5gqnEA4fD48T0fFMMACjkbLjAadw; rur="CCO\05466898393014\0541752420366:01f779b0d61c4cc0927c3d6175c39d5c68417043c415f79cfeda4c41b2617a9ae3b633bd"'
                               ,header=headers
                               )
        #192.168.31.28:9000
        self.ws.run_forever(http_proxy_host="192.168.31.28", http_proxy_port=9000, proxy_type='http',sslopt={"cert_reqs": ssl.CERT_NONE})


def get_token(cookie):

    url = "https://www.instagram.com/direct/inbox/"
    headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'cache-control': "max-age=0",
            'dpr': "1",
            'viewport-width': "500",
            'sec-ch-ua': "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'sec-ch-ua-platform-version': "\"10.0.0\"",
            'sec-ch-ua-model': "\"\"",
            'sec-ch-ua-full-version-list': "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
            'sec-ch-prefers-color-scheme': "light",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://www.google.com/",
            'priority': "u=0, i",
             #'Cooike':cookie,
             #'Cookie': "mid=Zmev2gALAAGx-m_pV0MGi938YII1; ig_did=8900DF60-BB30-4397-A184-49B26FA282B8; datr=2q9nZo279aFvIwMpodLj4i8K; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=14DMZwBOL8EbgKRQTKyyVurdnOv8SjOL; ds_user_id=66881971457; shbid=\"3441\\05466881971457\\0541752199519:01f7d019e08e168da954c6143ba03d34cc3ecffd2b5baa865c21e2dd9ab2eccbdd5cdc2b\"; shbts=\"1720663519\\05466881971457\\0541752199519:01f7796ec0c5745502b04592bcbd1b48ebad4954ac39f034c3f35f8bef0fcc7daac8e3c5\"; wd=500x623; sessionid=66881971457%3A8HydLZs19zsNLX%3A21%3AAYct4H0dB25022pPB7ntP0WeWDsulAfT9uwx_1R2dZM; rur=\"CCO\\05466881971457\\0541752292068:01f7cd0393c56f2ed6ceb6b4f0b1c86b2690dad06d8462b91c76400bb92b7149833b760f\""
            'Cookie':'mid=Zm-y1QAEAAGNHxST8H_JCHVykV7y; ig_did=A01806A7-2C0F-4928-970B-AE15EDAEEEA4; datr=1bJvZiOGH4ZJ2JnkCP17Q98E; ig_nrcb=1; csrftoken=8VKp1SN7fULQ1hBTkwmbI4VyoqNKqLrw; ds_user_id=66898393014; shbid="12767\05466898393014\0541752381644:01f7e73376330e907038d58beb2314bf7a4f1c2a38eb60346c4e0ba08e23eb2cb9907b79"; shbts="1720845644\05466898393014\0541752381644:01f7341b07e5352d70e5b797e356a12cc97f56c1680b2f96166b98856efe5a0f024c8916"; ps_n=1; ps_l=1; wd=1440x715; sessionid=66898393014%3AFx8xgxv6d0EQn3%3A26%3AAYfmmuh6dVAbkc5gqnEA4fD48T0fFMMACjkbLjAadw; rur="CCO\05466898393014\0541752420366:01f779b0d61c4cc0927c3d6175c39d5c68417043c415f79cfeda4c41b2617a9ae3b633bd"'

          }

    response = requests.get(url, headers=headers,verify=False)
    p1 =re.compile('{"clientID":"(.*?)"}')
    p2 =re.compile('"actorID":"(.*?)",')
    clientID= re.findall(p1,response.text)[0]
    actorID=re.findall(p2,response.text)[0]
    print(actorID) # actorID
    print(clientID)#
    return {'cid':clientID,'aid':actorID}

if __name__ == '__main__':
    with open('cookie.txt','r+',encoding='utf-8') as f:
        cookie =f.read()
    token = get_token(cookie)
    cid = token['cid']
    aid = token['aid']
    Test(cid,aid).start(cookie)


