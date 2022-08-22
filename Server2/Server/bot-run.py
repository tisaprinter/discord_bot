from urllib import request
from utils import db
import json, requests, time, math

API_URL = 'http://127.0.0.1:81/'

messages_log = []
last_check = 0
accounts = {
    'account1': {'token': ''},
    'account2': {'token': ''},
    'account3': {'token': ''},
    'account4': {'token': ''},
    'account5': {'token': ''}
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
    print("send messages")
    global last_check
    global accounts
    global messages_log

    token1 = db.get_value("value", "config", "name", "token1")
    token2 = db.get_value("value", "config", "name", "token2")
    token3 = db.get_value("value", "config", "name", "token3")
    token4 = db.get_value("value", "config", "name", "token4")
    token5 = db.get_value("value", "config", "name", "token5")

    token1 = token1.split("\n")[0]
    token2 = token2.split("\n")[0]
    token3 = token3.split("\n")[0]
    token4 = token4.split("\n")[0]
    token5 = token5.split("\n")[0]
    # print({"token1: %s, token2: %s"}, token1, token2)
    if not token1 or not token2 or not token3 or not token4 or not token5:
        sleep(1)
        return

    if token1 != accounts['account1']['token'] or token2 != accounts['account2']['token'] or token3 != accounts['account3']['token'] or token4 != accounts['account4']['token'] or token5 != accounts['account5']['token']:
        accounts['account1']['token'] = token1
        accounts['account2']['token'] = token2
        accounts['account3']['token'] = token3
        accounts['account4']['token'] = token4
        accounts['account5']['token'] = token5
        last_check = 0





    if last_check + 600 < time.time():
        # print("send message===>")
        ########## Check accounts validity
        for account in accounts:
            resp = requests.get("https://discord.com/api/v9/users/@me",  headers = {'authorization': accounts[account]['token'],'content-type': 'application/json'})
            if 'id' not in resp.text:
                return

            resp = resp.json()

            try:
                accounts[account]['id'] = resp['id']
                accounts[account]['username'] = resp['username']
            except:
                return
        ###################################
        print("Accounts verified")
        last_check = time.time()



    for conversation in db.get_value("*", "conversations", arr=True):

        if conversation[3] == True: continue # message sent flag
        else:
            messages = json.loads(conversation[2])


            for channel in db.get_value("*", "channels", arr=True):
                if is_off(): return
                channel_id = channel[0]


                #### check if channel is available and get the guild ID (used later in replies.)
                for account in accounts:
                    resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}",
                                        headers={'authorization': accounts[account]['token'],
                                                'content-type': 'application/json'})
                    if 'guild_id' not in resp.text: continue

                    resp = resp.json()
                    try:  guild_id = resp['guild_id']
                    except: continue


                    ###################################################################################
                    last_message_id = 0

                    for message in messages:
                        delete_old_messages()
                        if is_off(): return

                        sender_token = accounts[message['sender']]['token']
                        content = message['content']
                        # receiver_id = accounts['account2' if message['sender'] == 'account1' else 'account1']['id']
                        # receivers = [accounts[p]['username'] for p in accounts if p != message['sender']]
                        # print("receiver ids==>", receivers, content)
                        # receivername = ""
                        # for receiver in receivers:
                        #     receivername += f"@{receiver} "

                        # if message['response'] == 'mention':
                        #     content = f"{receivername} {content}"

                        data = {'content': content,"nonce":None,"tts":False}

                        # if message['response'] == 'reply' and accounts[message['receiver']]['token']:
                        if int(message['receiver']) > 0:
                            print("last_message_id 1")
                            resp_messages = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={'authorization': accounts[message['sender']]['token'], 'content-type': 'application/json'})
                            if not resp_messages:
                                return {'success': False, 'code': 400, 'message': f'Missing the following in channel\'s data:'}, 400
                            print("last_message_id 2", resp_messages)
                            # me = requests.get("https://discord.com/api/v9/users/@me", headers={'authorization': accounts['account3']['token'], 'content-type': 'application/json'})
                            # print("last_message_id 3", me.json())
                            # if 'id' not in me.text:
                            #     return

                            resp_messages = resp_messages.json()
                            # me = me.json()
                            # print(resp[0])
                            # last_message_id = [p for p in resp if p['author']['id'] == me['id']]
                            print("message['line'] - message['receiver']", int(message['line']) - int(message['receiver']))
                            reply_message = resp_messages[int(message['line']) - int(message['receiver'])]
                            # reply_message = last_message_id[0]
                            print("last_message_id 4", reply_message)
                            data['message_reference'] = {'channel_id': str(channel_id), 'guild_id': guild_id, 'message_id': reply_message['id']}

                        while True:
                            try:
                                print("message data", json.dumps(data))
                                resp = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages",
                                    headers={'authorization': sender_token, 'content-type': 'application/json'},
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

            requests.patch(F"{API_URL}/conversations/{conversation[0]}", data={'sent': True})

def sleep(duration):
    for i in range(math.floor(duration)):
        time.sleep(1)
        delete_old_messages()

    time.sleep(duration - math.floor(duration))
def main():
    while True:
        if not is_off():
            send_messages()
            # db.cmd("UPDATE config SET value=%s where name=%s", ("off", "status"))

        delete_old_messages()
        # print("sleep 500")
        time.sleep(1)

if __name__ == "__main__": main()
