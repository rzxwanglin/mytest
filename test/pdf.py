import threading
import time

import websocket

# socket访问地址：
socket_add = "wss://edge-chat.instagram.com/chat?sid=5545895126892543&cid=68195496-689d-41f3-8922-476697a727e2"

def on_message(ws, message):
    print(f"接收到消息：{message}")


def on_error(ws, error):
    # 程序报错时，就会触发on_error事件
    print(error)


def on_close(ws, param1, param2):
    print("Connection closed------")


def on_open(ws):
    ws.send(build_message("CONNECT", {"passcode": "", "accept-version": "1.0,1.1,1.2", "heart-beat": "5000,0"}))
    time.sleep(2)
    topic = "xxxxx"
    ws.send(build_message("SUBSCRIBE", {"id": "sub-0", "destination": topic}))

    # 启动心跳检测任务
    thread = threading.Thread(target=check_heartbeat, args=[ws])
    thread.start()


def check_heartbeat(ws):
    while True:
        time.sleep(5)
        ws.send(build_message("SEND", ''))
        print(f"心跳发送成功-------")


# 按照消息格式定义消息内容
def build_message(command, headers, msg=None):
    BYTE = {
        'LF': '\x0A',
        'NULL': '\x00',
        'HIDDEN': '\u0001'
    }
    data_arr = [command + BYTE['LF']]

    # add headers
    for key in headers:
        data_arr.append(key + ":" + headers[key] + BYTE['LF'])

    data_arr.append(BYTE['LF'])

    # add message, if any
    if msg is not None:
        data_arr.append(msg)

    # terminate with null octet
    data_arr.append(BYTE['NULL'])

    frame = ''.join(data_arr)

    # transmit over ws
    print("构建后数据：" + frame)

    return frame


def main(address=socket_add):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(address,
                                cookie="xxxxx",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever(ping_interval=5, ping_timeout=3)


if __name__ == "__main__":
    main()