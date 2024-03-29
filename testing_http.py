#!/usr/bin/env python3
import requests
from zipfile import ZipFile

r = requests.get("http://127.0.0.1:5800/api/settings/photonvision_config.zip")

print(f"Status code: {r.status_code}, is OK {r.ok}")

with open("settings.zip", "wb") as file:
    file.write(r.content)
