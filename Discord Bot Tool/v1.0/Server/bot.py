import sys, time, json, requests
from utils import db
bot_id   = sys.argv[1]
info = db.get_value("*", table="bots", search_filter="id", value=(int(bot_id),), arr=True)

info = info[0] if info else None

if not info: exit(1)

accounts = {
    'account1': {'token': info[2]},
    'account2': {'token': info[3]}
}

for account in accounts:
    resp = requests.get("https://discord.com/api/v9/users/@me",  headers = {'authorization': accounts[account]['token'],'content-type': 'application/json'})
    
    if 'id' not in resp.text:
        exit(2)
        
    resp = resp.json()
    
    try: 
        accounts[account]['id'] = resp['id']
    except:
        exit(3)
        

channel_id = info[4]

resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers={'authorization': accounts['account1']['token'], 'content-type': 'application/json'})

if 'guild_id' not in resp.text: exit(4)
        
resp = resp.json()

try: 
    guild_id = resp['guild_id']
except:
    exit(5)


resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers={'authorization': accounts['account2']['token'], 'content-type': 'application/json'})

if 'guild_id' not in resp.text: exit(4)



messages_log = []
while True:
    if not db.get_value("id", table="bots", search_filter="id", value=(int(bot_id),)):
        exit(2)
        
    if db.get_value("value", table="options", search_filter="name", value=("status",)) == "off":
        continue
        
    random_conversation = db.get_value("messages", table="conversations", order="RAND()")
    
    
    try: random_conversation = json.loads(random_conversation)
    except:
        time.sleep(10)
        continue
    
    
    last_message_id = 0
    for message in random_conversation:
        if db.get_value("value", table="options", search_filter="name", value=("status",)) == "off": break
        if not db.get_value("id", table="bots", search_filter="id", value=(int(bot_id),)):
            exit(2)
        
        token = accounts[message['sender']]['token']
        
        content = message['content']
        receiver_id = accounts['account2' if message['sender'] == 'account1' else 'account1']['id']
        
        
        if message['response'] == 'mention':
            content = f"<@{receiver_id}> {content}"
        
        data = {'content': content,"nonce":None,"tts":False}
        
        if message['response'] == 'reply':
            data['message_reference'] = {'channel_id': str(channel_id), 'guild_id': guild_id, 'message_id': last_message_id}
            
        while True: 
            try:
                resp = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                    headers={'authorization': token, 'content-type': 'application/json'},
                    data = json.dumps(data)
                )
                break
            except:
                time.sleep(5)
                continue
                
        try: 
            last_message_id = resp.json()['id']
            messages_log.append({'time': time.time(), 'id': last_message_id})
        except: 
            print(f"REPORT: Failed to send message: {content}.\nReturned response: {resp.text}.\n============================")
        time.sleep(float(message['delay']))
    
    
    new_messages = []
    for message in messages_log:
        if message['time'] > time.time() - 3600: 
            new_messages.append(message)
            continue
        while True: 
            try:
                resp = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message['id']}", 
                    headers={'authorization': token, 'content-type': 'application/json'}
                )
                break
            except:
                time.sleep(5)
                continue  
        time.sleep(1.5)
        
    messages_log = new_messages
        
        
    
    time.sleep(10)
