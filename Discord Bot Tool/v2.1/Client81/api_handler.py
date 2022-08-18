import requests

#API_URL = "http://185.80.53.196:81/"
API_URL='http://127.0.0.1:81/'

# BOTS
def get_bots():
    """Get all bots from the API
    """
    r = requests.get(API_URL + '/channels')

    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data

# # print(get_bots())

def post_bots(name, account1_token, account2_token, account3_token, account4_token, account5_token, channel_id):
    """Post a new bot to the API
    """
    data = {
        'name': name,
        'account1_token': account1_token,
        'account2_token': account2_token,
        'account3_token': account3_token,
        'account4_token': account4_token,
        'account5_token': account5_token,
        'channel_id': channel_id
    }
    r = requests.post(API_URL + '/bots', json=data)

    # # print(r.json())

    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data

def delete_bot(id):
    """Delete a bot from the API
    """
    r = requests.delete(API_URL + '/channels/' + str(id))

    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data

# Conversations
def get_conversations():
    """Get all conversations from the API
    """
    r = requests.get(API_URL + '/conversations')
    
    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data

def post_conversations(name, messages):
    """Post a new conversation to the API
    """
    data = {
        'name': name,
        'messages': messages
    }
    r = requests.post(API_URL + '/conversations', json=data)
    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data

def delete_conversation(id):
    """Delete a new conversation to the API
    """
    # print("delete_conversation:", id)
    r = requests.delete(API_URL + '/conversations/' + str(id),)
    
    if r.status_code >= 200 and r.status_code < 300:
        data = r.json()
    else:
        try:
            data = r.json()
            # data = {"success": "false", "message": "Error " + str(r.status_code)}
        except:
            data = {"success": "false", "message": "Error " + str(r.status_code)}
    return data