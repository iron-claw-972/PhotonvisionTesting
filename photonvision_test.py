#!/usr/bin/env python3
import websockets
import asyncio
import msgpack
import json
import sys


# Constants for terminal colors
TEXT_BOLD = '\033[1m'
COLOR_BLUE = '\033[94m'
COLOR_YELLOW = '\033[93m'
COLOR_OK = TEXT_BOLD + '\033[32m'
COLOR_BAD = TEXT_BOLD + '\033[31m'
COLOR_END = '\033[0m'


# TODO: Stop using a global variable
photon_settings = {}
expected_settings = None


# Function to display settings
def display_settings(settings: dict, camera_index: int):
    global expected_settings
    camera_name = settings["cameraSettings"][camera_index]["nickname"]
    if "port" in camera_name.lower():
        settings_file = open("expected-port.json")
    elif "starboard" in camera_name.lower():
        settings_file = open("expected-starboard.json")
    else:
        print("Unexpected Camera Name " + camera_name)
        settings_file = open("expected-port.json")

    expected_settings = json.load(settings_file)
    settings_file.close()
    
    pipeline_name = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["pipelineNickname"]
    camera_format_index = settings["cameraSettings"][camera_index]["currentPipelineSettings"]["cameraVideoModeIndex"]

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

    check_and_print_setting("Pipeline Name", pipeline_name)

    print_video_format(settings, camera_index, camera_format_index)

    check_and_print_setting("Doing Multi-Target", doing_multi_target)
    check_and_print_setting("Decision margin", decision_margin)
    check_and_print_setting("Auto Exposure", auto_exposure)
    check_and_print_setting("Camera exposure", camera_exposure)
    check_and_print_setting("Camera Brightness", camera_brightness)
    check_and_print_setting("Decimate", decimate)
    check_and_print_setting("Blur", blur)
    check_and_print_setting("Threads", threads)
    check_and_print_setting("Refine Edges", refine_edges)
    check_and_print_setting("Pose Estimation Iterations", pose_estimation_iterations)

def check_and_print_setting(key: str, value: any):
    if value == expected_settings[key]:
        print(f"{key}: {COLOR_OK}{value}{COLOR_END}")
    else:
        print(f"{key}: {COLOR_BAD}{value}{COLOR_END} (expected: {expected_settings[key]})")

def print_video_format(settings: dict, camera_index: int, format_index: int):
    video_format_list = settings["cameraSettings"][camera_index]["videoFormatList"]
    
    video_width = video_format_list[str(format_index)]["width"]
    video_height = video_format_list[str(format_index)]["height"]
    fps = video_format_list[str(format_index)]["fps"]
    pixel_format = video_format_list[str(format_index)]["pixelFormat"]

    formatted = f"{video_width} x {video_height} @ {fps}fps, {pixel_format}"
    check_and_print_setting("Target Resolution", formatted)


# Async function to get websocket data
async def listen(ip):
    url = "ws://" + ip +":5800/websocket_data"

    async with websockets.connect(url) as ws:
        global photon_settings
        
        for i in range(maxattempts := 10):
            
            msg = await ws.recv()
            unpacked = msgpack.unpackb(msg)

            photon_settings = unpacked
            if "settings" in photon_settings.keys():
                break
            elif i == maxattempts-1:
                raise Exception(f"No settings were found after {i} iterations.")




if len(sys.argv) > 1:
    ip_address = sys.argv[1]
else:
    ip_address = str(input("Enter device IP (no http:// or :5800): "))

asyncio.get_event_loop().run_until_complete(listen(ip_address))


print(f"{'*' * 50} {TEXT_BOLD}Photonvision settings check{COLOR_END} {'*' * 50}")

print(COLOR_BLUE + "Hostname: " + photon_settings["settings"]["networkSettings"]["hostname"] + COLOR_END)


if photon_settings["cameraSettings"][0] != None:
    display_settings(photon_settings, 0)

elif photon_settings["cameraSettings"][1] != None:
    display_settings(photon_settings, 1)

