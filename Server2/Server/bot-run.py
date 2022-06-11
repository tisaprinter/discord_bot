from utils import db
import json, requests, time, math


messages_log = []
last_check = 0
accounts = {
    'account1': {'token': ''},
    'account2': {'token': ''}
}


def is_off():
    return db.get_value("value", table="config", search_filter="name", value=("status",)) == "off"
                
def delete_old_messages():
    global messages_log
    new_messages = []
        
    for message in messages_log:
        if message['time'] + 3600 > time.time():    
            new_messages.append(message)
            continue
        while True: 
            try:
                resp = requests.delete(f"https://discord.com/api/v9/channels/{message['channel_id']}/messages/{message['id']}", 
                    headers={'authorization': message['author']['token'], 'content-type': 'application/json'}
                )
                break
            except:
                time.sleep(1)
                continue  
            
    messages_log = new_messages
        
                    
def send_messages():
    global last_check
    global accounts
    global messages_log
    
    token1 = db.get_value("value", "config", "name", "token1")
    token2 = db.get_value("value", "config", "name", "token2")

    if not token1 or not token2: 
        sleep(1)
        return
    
    if token1 != accounts['account1']['token'] or token2 != accounts['account2']['token']:
        accounts['account1']['token'] = token1
        accounts['account2']['token'] = token2
        last_check = 0
        
        
    


    if last_check + 600 < time.time():        
        ########## Check accounts validity
        for account in accounts:
            resp = requests.get("https://discord.com/api/v9/users/@me",  headers = {'authorization': accounts[account]['token'],'content-type': 'application/json'})
            
            if 'id' not in resp.text:
                return 
                
            resp = resp.json()
            
            try: 
                accounts[account]['id'] = resp['id']
            except:
                return
        ###################################
        print("Accounts verified")
        last_check = time.time()
    


    for conversation in db.get_value("*", "conversations", arr=True):
        
        messages = json.loads(conversation[2])
        
        
        for channel in db.get_value("*", "channels", arr=True):  
            if is_off(): return
            channel_id = channel[0]
            
            #### check if channel is available and get the guild ID (used later in replies.)
            resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers={'authorization': accounts['account1']['token'], 'content-type': 'application/json'})
            if 'guild_id' not in resp.text: continue
            
            resp = resp.json()
            try:  guild_id = resp['guild_id']
            except: continue
            
            #### Check if both tokens have access to the channel
            resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers={'authorization': accounts['account2']['token'], 'content-type': 'application/json'})
            if 'guild_id' not in resp.text: continue
        
        
            ###################################################################################
            last_message_id = 0
            
            for message in messages:
                delete_old_messages()
                if is_off(): return
                
                token = accounts[message['sender']]['token']    
                content = message['content']
                receiver_id = accounts['account2' if message['sender'] == 'account1' else 'account1']['id']

                if message['response'] == 'mention':
                    content = f"<@{receiver_id}> {content}"
                
                data = {'content': content,"nonce":None,"tts":False}
                
                if message['response'] == 'reply' and last_message_id:
                    data['message_reference'] = {'channel_id': str(channel_id), 'guild_id': guild_id, 'message_id': last_message_id}
                    
                while True: 
                    try:
                        resp = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                            headers={'authorization': token, 'content-type': 'application/json'},
                            data = json.dumps(data)
                        )
                        break
                    except:
                        sleep(5)
                        continue
                try: 
                    last_message_id = resp.json()['id']
                    messages_log.append({'time': time.time(), 'author': accounts[message['sender']], 'id': last_message_id, 'channel_id': channel_id})
                except: break
                    
                sleep(float(message['delay']))
                
def sleep(duration):
    for i in range(math.floor(duration)):
        time.sleep(1)
        delete_old_messages()
    
    time.sleep(duration - math.floor(duration))
def main():
    while True:
        if not is_off(): 
            send_messages()
            db.cmd("UPDATE config SET value=%s where name=%s", ("off", "status"))
    
        delete_old_messages()
    
if __name__ == "__main__": main()
