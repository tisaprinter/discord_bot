from utils import db
import subprocess, sys, time
status = "off"


while True:
    
    new_status = db.get_value("value", "config", "name", "status")
    
    if new_status == "off": 
        status = "off"
        continue
    
    if status == "on": continue
    
    if status == "off" and new_status == "on":
        subprocess.Popen([sys.executable, 'bot-run.py'])
        
    time.sleep(5)
    