from utils import db
import subprocess, sys, time
import os
status = "off"
cwd = os.getcwd()


while True:

    new_status = db.get_value("value", "config", "name", "status")

    if new_status == "off":
        status = "off"
        continue

    if status == "on":
        print("running bot", status)
        continue

    if status == "off" and new_status == "on":
        print("start bot run", status)
        status = "on"
        subprocess.Popen([sys.executable, f"{cwd}\\Server2\\Server\\bot-run.py"])

    time.sleep(100)
