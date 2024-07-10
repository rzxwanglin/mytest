import asyncio
import websockets

async def connect_to_websocket(uri):
    async with websockets.connect(uri) as websocket:
        # 发送消息
        await websocket.send("Hello, WebSocket!")
        print("Message sent to the server.")

        # 接收消息
        response = await websocket.recv()
        print(f"Message received from server: {response}")

# WebSocket服务器的URI
uri = "ws://localhost:8765"

# 运行WebSocket客户端
asyncio.get_event_loop().run_until_complete(connect_to_websocket(uri))
