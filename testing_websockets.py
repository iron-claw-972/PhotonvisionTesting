#!/usr/bin/env python3
import websockets
import asyncio 
import umsgpack

async def listen():
	url = "ws://localhost:5800/websocket_data"

	async with websockets.connect(url) as ws:
		for i in range(10):
			print(f"{'*' * 50} {i} {'*' * 50}")
			msg = await ws.recv()
			#print(msg)
			unpacked = umsgpack.unpackb(msg)
			print(unpacked)

asyncio.get_event_loop().run_until_complete(listen())

# with connect("ws://localhost:5800/websocket_data") as websocket:
#	 websocket.send("Hi")
#	 message = websocket.recv()
#	 print(f"Recieved: {message}")
