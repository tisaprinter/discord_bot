import asyncio
from utils import db
import subprocess, sys, time
import os
status = "off"
cwd = os.getcwd()


while True:

    global proc

    new_status = db.get_value("value", "config", "name", "status")

    print("running bot: ", status)
    time.sleep(1)

    if status == "off" and new_status == "on":
        print("start bot run", status)
        status = "on"
        proc = subprocess.Popen([sys.executable, f"{cwd}\\Server2\\Server\\bot-run.py"])

    if new_status == "off":
        status = "off"
        if proc: proc.kill()
        continue

    if status == "on":
        continue

