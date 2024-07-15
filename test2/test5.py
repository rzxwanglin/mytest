import time

import websocket
import base64
import os
import asyncio
import websockets
from aiohttp import ClientSession
import websocket
import struct
import asyncio
import websockets
def write_uint16_be(a, b, c):
    b[c] = a >> 8
    b[c + 1] = a % 256
    return c + 2

def utf8_length(s):
    length = 0
    for char in s:
        code = ord(char)
        if code < 128:
            length += 1
        elif code < 2048:
            length += 2
        elif 55296 <= code <= 56319:
            length += 4
            continue  # Skip the next character in the surrogate pair
        else:
            length += 3
    return length

def write_string(a, a_len, b, c):
    def h(a, b, c):
        b[c] = a >> 8
        b[c + 1] = a % 256
        return c + 2

    def j(a, b, c):
        for char in a:
            code = ord(char)
            if code < 128:
                b[c] = code
                c += 1
            elif code < 2048:
                b[c] = 192 | code >> 6
                b[c + 1] = 128 | code & 63
                c += 2
            elif code < 55296 or code >= 57344:
                b[c] = 224 | code >> 12
                b[c + 1] = 128 | code >> 6 & 63
                b[c + 2] = 128 | code & 63
                c += 3
            else:
                code = 65536 + ((code & 1023) << 10 | ord(a[c + 1]) & 1023)
                b[c] = 240 | code >> 18
                b[c + 1] = 128 | code >> 12 & 63
                b[c + 2] = 128 | code >> 6 & 63
                b[c + 3] = 128 | code & 63
                c += 4

    d = h(a_len, b, c)
    j(a, b, d)
    return d + a_len

def encode(mythis):
    i = [0, 6, 77, 81, 73, 115, 100, 112, 3]
    b = 16
    client_id_len = utf8_length(mythis['clientId'])
    username_len = utf8_length(mythis['connectOptions']['userName'])
    total_len = 12 + client_id_len + 2 + username_len + 2
    e = [177, 3]
    c = bytearray(total_len + len(i) + len(e) + 10)  # Allocate enough space
    f = c
    f[0] = b
    b = 1
    f[b:b + len(e)] = e
    b += len(e)
    f[b:b + len(i)] = i
    b += len(i)
    e = 2 | 128
    f[b] = e
    b += 1
    b = write_uint16_be(15, f, b)
    b = write_string("mqttwsclient", utf8_length("mqttwsclient"), f, b)
    b = write_string(mythis['connectOptions']['userName'], username_len, f, b)
    return bytes(c)

def connect(b, c):
    return {
        'messageType': 1,
        'clientId': 'mqttwsclient',
        'connectOptions': c
    }

# a_ = {
#     "ignoreSubProtocol": True,
#     "mqttVersion": 3,
#     "userName": '{"a":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"68195496-689d-41f3-8922-476697a727e2","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":5545895126892543,"st":[],"u":"17841466750442299"}'
# }
# mythis = connect(None, a_)
# encoded_message = encode(mythis)
# print(encoded_message)
# print(type(encoded_message))


url = "wss://edge-chat.instagram.com/chat?sid=2969472774176767&cid=94c0a708-cf68-4d0f-a08d-f0f1d5a02897"
headers = [
    'Pragma: no-cache',
    'Cache-Control: no-cache',
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Encoding: gzip, deflate, br, zstd',
    'Accept-Language: zh-CN,zh;q=0.9',
    'Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits',
    'Cookie:ig_did=76DFB32F-D234-4309-88AA-E6085C5374C6; datr=7T9pZoYHevj9WSFhe-s9Lhsz; mid=Zmk_8gALAAEQ4k_rOLpfRB5FrTG4; ig_nrcb=1; csrftoken=FZGIoEaEpeQCbe0cj6tEmMkGpm6wIQWN; ds_user_id=66898393014; shbid="12767\05466898393014\0541751946935:01f7175bf8b59f18c60dad0fac890a2d709f8f8b42efc61f1563365e846b0cbac58ce794"; shbts="1720410935\05466898393014\0541751946935:01f7133519b38846542e1627147181f396a73dd6449a087890f5541d26d279b842055d6a"; ps_n=1; ps_l=1; wd=861x755; sessionid=66898393014%3AY2FdkTsrtNzsOj%3A0%3AAYf9W9qm9g_L8OeGOT0QwriUjfBGuxOMJipuDCZKe5U; rur="CCO\05466898393014\0541752205853:01f705ffdc24e60d87b0cfe1961ec725723f964f49eb217249511477d3d7ea7ec857d238"'
]

try:
    ws = websocket.create_connection(url, header=headers,http_proxy_host='172.17.32.1',http_proxy_port=9000)
    print("WebSocket connection established")
    a_ = {
        "ignoreSubProtocol": True,
        "mqttVersion": 3,
        "getKeepAliveIntervalSeconds":"ƒ()",
        "getKeepAliveTimeoutSeconds":"ƒ()",
        "onConnectFailure":"ƒ(c, d, g)",
        "onConnectSuccess":"ƒ(c)",
        "onConnection":"ƒ()",
        "onConnectionLost":"ƒ(b, c)",
        "onMessageArrived":"ƒ(b, c, d)",
        "onMessageDelivered":"ƒ(b)",
        #"userName": '{"a":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"6fa3ee9d-3ef9-42f2-923f-d21906ffa19c","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":5545895126892543,"st":[],"u":"17841466750442299"}'
        #"userName":'{"a":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"94c0a708-cf68-4d0f-a08d-f0f1d5a02897","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":2969472774176767,"st":[],"u":"17841466823730246"}',
        "userName":'{"a":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"99ccd4af-e54c-4a4f-8cf8-fb4ba514d3c5","dc":"","ecp":10,"fg":true,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":2106728063696895,"st":[],"u":"17841466750442299"}'
    }
    mythis = connect(None, a_)
    encoded_message = encode(mythis)
    print(encoded_message)
    print(type(encoded_message))
    # Example of sending a message
    ws.send(encoded_message)



    print("Sent a message")
    # Example of receiving a message
    while True:
        try:
            response = ws.recv()
            print(type(response))
            print(len(response))
            print("Received a message: ", response)
            time.sleep(1)
            ws.send(encoded_message)
            print("Sent a message")
        except Exception as e:
            print(e)
            time.sleep(1)

    ws.close()
except websocket.WebSocketBadStatusException as e:
    print(f"Failed to establish WebSocket connection: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
