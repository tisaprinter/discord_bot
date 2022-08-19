from flask import Flask, request

from utils import db
import json


app = Flask(__name__)


@app.route('/conversations', methods=["GET"])
def get_conversations():
    conversations = db.get_value("*", table="conversations", arr=True)
    data = []

    for conversation in conversations:
        data.append({'id': conversation[0],'name': conversation[1]})

    return {'success': True, 'data': data}


@app.route('/conversations', methods=["POST"])
def add_conversations():
    request_data = {}
    try:
        request_data = request.get_json(force=True)
    except:
        ...
    if not request_data: return {'success': False, 'code': 400, 'message': f"Could not parse json data from request."}, 400

    missing_data = []

    required_data = ['name', 'messages', 'sent']

    for datum in required_data:
        if datum not in request_data: missing_data.append(datum)

    if missing_data:
        return {'success': False, 'code': 400, 'message': f'Missing the following in request\'s json: {missing_data}'}, 400

    if not isinstance(request_data['messages'], list):
        return {'success': False, 'code': 400, 'message': f"messages must be a list."}

    messages = request_data['messages']

    if not messages:
        return {'success': False, 'code': 400, 'message': f'conversation must include at least one message.'}, 400

    required_data = ['content', 'sender', 'receiver', 'delay', 'response']
    for message in messages:
        missing_data = []
        for datum in required_data:
            if datum not in message: missing_data.append(datum)

        if missing_data:
            return {'success': False, 'code': 400, 'message': f'Missing the following in message[{messages.index(message)}]\'s data: {missing_data}'}, 400

        if message['sender'] not in ["account1", "account2", "account3", "account4", "account5"]:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. sender must be \'account1\' or \'account2\' or \'account3\' or \'account4\' or \'account5\''}, 400

        # if message['receiver'] not in ["account1", "account2", "account3", "account4", "account5"]:
        #     return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. receiver must be \'account1\' or \'account2\' or \'account3\' or \'account4\' or \'account5\''}, 400

        try:
            float(message['delay'])
        except:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. delay must be float or int'}, 400
        message['response'] = message['response'].lower()
        if message['response'] not in ["mention", "reply", "neutral"]:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. response must be \'mention\', \'reply\', or \'neutral\''}, 400

        # if messages.index(message) == 0:
        #     if message['response'] not in ['mention', 'neutral']:
        #         print(message['response'])
        #         return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. response must be \'mention\' or \'neutral\''}, 400

        if not message['content']:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. content cannot be empty'}, 400


    sent = request_data['sent']

    print("post conversations", sent)

    if sent:
        return {'success': False, 'code': 400, 'message': f'new conversation must send at least one message.'}, 400


    db.cmd("INSERT INTO conversations VALUES(%s, %s, %s, %s)", value=(None, request_data['name'], json.dumps(request_data['messages']), request_data['sent']))

    conversation_id = db.get_value("id", table="conversations", order="id DESC")
    return {'success': True, 'id': conversation_id}


@app.route("/conversations/<int:conversation_id>", methods=["PATCH"])
def patch_conversations(conversation_id):
    print("patch converstation", conversation_id)
    db.cmd("UPDATE conversations SET sent=%s WHERE id=%s", (True, conversation_id))

    return {'success': True}

@app.route('/conversations/<int:conversation_id>', methods=["DELETE"])
def delete_conversation(conversation_id):
    db.cmd("DELETE FROM conversations WHERE id=%s", value=(conversation_id,))
    return {'success': True}

################################################################################################################################

@app.route("/config", methods=["GET"])
def get_config():
    status = db.get_value("value", "config", "name", "status")
    token1 = db.get_value("value", "config", "name", "token1")
    token2 = db.get_value("value", "config", "name", "token2")
    token3 = db.get_value("value", "config", "name", "token3")
    token4 = db.get_value("value", "config", "name", "token4")
    token5 = db.get_value("value", "config", "name", "token5")


    return {'success': True, 'data': {'status': status, 'token1': token1, 'token2': token2, 'token3': token3, 'token4': token4, 'token5': token5}}


@app.route("/config", methods=["PATCH"])
def patch_config():
    try: request_data = request.get_json(force=True)
    except: request_data = {}


    required_data = ['token1', 'token2', 'token3', 'token4', 'token5', 'status']
    missing_data = []


    for datum in required_data:
        if datum not in request_data: missing_data.append(datum)

    if missing_data:
        return {'success': False, 'code': 400, 'message': f'Missing the following in request\'s json: {missing_data}'}, 400

    for datum in request_data:
        if not request_data[datum]: return {'success': False, 'code': 400, 'message': f"{datum} cannot be empty."}, 400

    if request_data['status'] not in ["on", "off"]:
        return {'success': False, 'code': 400, 'message': f"status must either be 'on' or 'off'"}, 400

    print(request_data)

    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['status'], 'status'))
    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['token1'], 'token1'))
    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['token2'], 'token2'))
    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['token3'], 'token3'))
    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['token4'], 'token4'))
    db.cmd("UPDATE config SET value=%s WHERE name = %s", (request_data['token5'], 'token5'))

    return {'success': True}



################################################################################################################################


@app.route('/channels', methods=["GET"])
def get_channels():
    channels = db.get_value("*", table="channels", arr=True)
    data = []

    for channel in channels:
        data.append(channel[0])

    return {'success': True, 'data': data}



@app.route('/channels', methods=["POST"])
def post_channel():
    try: request_data = request.get_json(force=True)
    except: request_data = {'channels': []}

    if 'channels' not in request_data:
        return {'success': False, 'code': 400, 'message': f'Missing the following in request\'s json: \'channels\''}, 400

    for channel in request_data['channels']:
        if db.get_value("channel_id", "channels", "channel_id", channel): continue
        db.cmd("INSERT INTO channels VALUES (%s)", channel)


    return {'success': True}


@app.route('/channels/<channel_id>', methods=["DELETE"])
def delete_channel(channel_id):
    db.cmd("DELETE FROM channels WHERE channel_id=%s", value=(channel_id,))
    return {'success': True}

app.run('0.0.0.0', port=81)
