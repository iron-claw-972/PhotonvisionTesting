import websockets
import asyncio 

async def listen():
    url = "ws://localhost:5800/websocket_data"

    async with websockets.connect(url) as ws:
        for i in range(10):
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())

# with connect("ws://localhost:5800/websocket_data") as websocket:
#     websocket.send("Hi")
#     message = websocket.recv()
#     print(f"Recieved: {message}")