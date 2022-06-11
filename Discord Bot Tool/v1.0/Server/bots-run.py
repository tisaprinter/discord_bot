import subprocess
import sys
from utils import db
import time

active_bots = []

while True:
    bots = db.get_value("id", table="bots", arr=True)

    for bot in bots: 
        if bot in active_bots: continue
        subprocess.Popen([sys.executable, "bot.py", str(bot)])
        active_bots.append(bot)
        
    time.sleep(5)
    
    
    