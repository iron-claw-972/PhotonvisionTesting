#!/usr/bin/env python3
import websockets
import asyncio
import msgpack

# Constants for terminal colors
TEXT_BOLD = '\033[1m'
COLOR_BLUE = '\033[94m'
COLOR_YELLOW = '\033[93m'
COLOR_END = '\033[0m'


# TODO: Stop using a global variable
photon_settings = {}



def display_settings(settings: dict, camera_index: int):
    camera_name = settings["cameraSettings"][camera_index]["nickname"]

    pipeline_name = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["pipelineNickname"]
    doing_multi_target = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["doMultiTarget"]
    decision_margin = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["decisionMargin"]
    auto_exposure = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["cameraAutoExposure"]
    camera_exposure = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["cameraExposure"]
    camera_brightness = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["cameraBrightness"]
    threads = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["threads"]
    decimate = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["decimate"]
    blur = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["decimate"]
    refine_edges = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["refineEdges"]
    pose_estimation_iterations = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["numIterations"]


    print(f"{'*' * 30} {TEXT_BOLD}Settings for {COLOR_BLUE}{camera_name}{COLOR_END}: {'*' * 30}")

    print_setting("Pipeline Name", pipeline_name)
    print_setting("Doing Multi-Target", doing_multi_target)
    print_setting("Decision margin", decision_margin)
    print_setting("Auto Exposure", auto_exposure)
    print_setting("Camera exposure", camera_exposure)
    print_setting("Camera Brightness", camera_brightness)
    print_setting("Decimate", decimate)
    print_setting("Blur", blur)
    print_setting("Threads", threads)
    print_setting("Refine Edges", refine_edges)
    print_setting("Pose Estimation Iterations", pose_estimation_iterations)

def print_setting(key: str, value: any):
    print(TEXT_BOLD + f"{key}: {COLOR_YELLOW}{value}" + COLOR_END)


async def listen(ip):
    url = "ws://" + ip +":5800/websocket_data"

    async with websockets.connect(url) as ws:
        global photon_settings
        
        for i in range(10):
            
            msg = await ws.recv()
            unpacked = msgpack.unpackb(msg)

            photon_settings = unpacked
            if "settings" in photon_settings.keys():
                break




ip_address = str(input("Enter device IP (no http:// or :5800): "))

asyncio.get_event_loop().run_until_complete(listen(ip_address))


print(f"{'*' * 50} {TEXT_BOLD}Photonvision settings check{COLOR_END} {'*' * 50}")

print(COLOR_BLUE + "Hostname: " + photon_settings["settings"]["networkSettings"]["hostname"] + COLOR_END)


if photon_settings["cameraSettings"][0] != None:
    display_settings(photon_settings, 0)

elif photon_settings["cameraSettings"][1] != None:
    display_settings(photon_settings, 1)

