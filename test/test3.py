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

# 示例使用
# mythis = connect(None, {'userName': 'testuser'})
# encoded_message = encode(mythis)
# print(encoded_message)
import asyncio
import aiohttp
import websockets

# 编码函数和连接选项设置略...

async def connect_to_websocket_with_proxy(uri, proxy):
    # 创建 aiohttp.ClientSession 以设置代理
    async with aiohttp.ClientSession() as session:
        # 使用 aiohttp 的代理设置来创建 WebSocket 连接
        async with websockets.connect(
            uri,
            ssl=False,  # 如果 WebSocket 是非加密的，设置为 False
        ) as websocket:
            # 发送和接收消息的逻辑
            a_ = {
                "ignoreSubProtocol": True,
                "mqttVersion": 3,
                "userName": '{"a":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","aid":936619743392459,"aids":null,"chat_on":true,"cp":3,"ct":"cookie_auth","d":"68195496-689d-41f3-8922-476697a727e2","dc":"","ecp":10,"fg":false,"gas":null,"mqtt_sid":"","no_auto_fg":true,"p":null,"pack":[],"php_override":"","pm":[],"s":5545895126892543,"st":[],"u":"17841466750442299"}'
            }
            mythis = connect(None, a_)
            encoded_message = encode(mythis)
            print(encoded_message)
            print(type(encoded_message))

            await websocket.send(encoded_message)
            print("Message sent to the server.")
            response = await websocket.recv()
            print(f"Message received from server: {response}")

# WebSocket 服务器的URI
uri = "wss://edge-chat.instagram.com/chat?sid=5545895126892543&cid=68195496-689d-41f3-8922-476697a727e2"

# HTTP 代理的配置
class ProxyConfig:
    def __init__(self, url, auth=None):
        self.url = url
        self.auth = auth

# HTTP 代理的地址和认证信息（如果需要）
proxy_url = "http://127.0.0.1:10900"
proxy_auth = None  # 如果代理需要认证，填写用户名和密码的元组，例如 ("username", "password")

# 创建代理配置对象
proxy = ProxyConfig(proxy_url, proxy_auth)

# 运行 WebSocket 客户端连接
asyncio.get_event_loop().run_until_complete(connect_to_websocket_with_proxy(uri, proxy))
