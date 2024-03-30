#!/usr/bin/env python3
import websockets
import asyncio 
import umsgpack
import msgpack
import json
import time

photon_settings = {}

async def listen():
    url = "ws://localhost:5800/websocket_data"

    async with websockets.connect(url) as ws:
        global photon_settings
        
        for i in range(2):
            # print(f"{'*' * 50} {i} {'*' * 50}")
            msg = await ws.recv()
            # print(msg)
            
            unpacked = msgpack.unpackb(msg)
            # print(unpacked)
            
            if i == 1:
                photon_settings = unpacked



asyncio.get_event_loop().run_until_complete(listen())



print("Hostname: " + photon_settings["settings"]["networkSettings"]["hostname"])
print(f"{'*' * 50}")
print(photon_settings["cameraSettings"][0]["nickname"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["pipelineNickname"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["doMultiTarget"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["decisionMargin"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["cameraAutoExposure"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["cameraExposure"])
print(photon_settings["cameraSettings"][0]["currentPipelineSettings"]["cameraBrightness"])
