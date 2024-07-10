import asyncio
import websockets
from aiohttp import ClientSession
import websocket
import time
import json
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
    c = 12 + utf8_length(mythis['clientId']) + 2 + utf8_length(mythis['connectOptions']['userName']) + 2
    e = [177, 3]
    c = bytearray(436)
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
    b = write_string(mythis['connectOptions']['userName'], utf8_length(mythis['connectOptions']['userName']), f, b)
    return bytes(c)

def connect(b, c):
    return {
        'messageType': 1,
        'clientId': 'mqttwsclient',
        'connectOptions': c
    }


url = "wss://edge-chat.instagram.com/chat?sid=5545895126892543&cid=68195496-689d-41f3-8922-476697a727e2"

headers= {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
proxy = 'http://127.0.0.1:10900'
ws = websocket.create_connection(url=url,headers=headers, proxy=proxy,timeout=15)
print(ws.recv())
a_ = {
    "ignoreSubProtocol": True,
    "mqttVersion": 3,
    "userName": '{"a":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"68195496-689d-41f3-8922-476697a727e2","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":5545895126892543,"st":[],"u":"17841466750442299"}'

}
mythis = connect(None, a_)
encoded_message = encode(mythis)
print(encoded_message)
print(type(encoded_message))

ws.send()  # 以字符串发送消息
for i in range(100):
    print(ws.recv())
    time.sleep(1)
ws.close()  # 关闭连接