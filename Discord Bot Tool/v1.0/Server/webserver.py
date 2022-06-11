from flask import Flask, request

from utils import db
import json

app = Flask(__name__)


@app.route('/bots', methods=["GET"])
def get_bots(): 
    bots = db.get_value("*", table="bots", arr=True)
    data = []
    
    for bot in bots:
        data.append({'id': bot[0],'name': bot[1]})
        
    return {'success': True, 'data': data}



@app.route('/bots', methods=["POST"])
def add_bots(): 
    request_data = {}
    try:
        request_data = request.get_json(force=True)
    except:
        ...
    if not request_data: return {'success': False, 'code': 400, 'message': f"Could not parse json data from request."}, 400

    missing_data = []
    
    required_data = ['name', 'account1_token', 'account2_token', 'channel_id']
    
    for datum in required_data:
        if datum not in request_data: missing_data.append(datum)
        
    if missing_data:
        return {'success': False, 'code': 400, 'message': f'Missing the following in request\'s json: {missing_data}'}, 400
    
    if not request_data['channel_id'].isdigit():
        return {'success': False, 'code': 400, 'message': f"channel_id must be of type int."}
    
    db.cmd("INSERT INTO bots VALUES(%s, %s, %s, %s, %s)", value=(None, request_data['name'], request_data['account1_token'], request_data['account2_token'], int(request_data['channel_id'])))
    bots_id = db.get_value("id", table="bots", order="id DESC")
    return {'success': True, 'id': bots_id}


@app.route('/bots/<int:bot_id>', methods=["DELETE"])
def delete_bot(bot_id): 
    db.cmd("DELETE FROM bots WHERE id=%s", value=(bot_id,))
    return {'success': True}



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
    
    required_data = ['name', 'messages']
    
    for datum in required_data:
        if datum not in request_data: missing_data.append(datum)
        
    if missing_data:
        return {'success': False, 'code': 400, 'message': f'Missing the following in request\'s json: {missing_data}'}, 400
    
    if not isinstance(request_data['messages'], list):
        return {'success': False, 'code': 400, 'message': f"messages must be a list."}
    
    messages = request_data['messages']
    
    if not messages:
        return {'success': False, 'code': 400, 'message': f'conversation must include at least one mesage.'}, 400
    
    required_data = ['content', 'sender', 'delay', 'response']
    for message in messages:
        missing_data = []
        for datum in required_data: 
            if datum not in message: missing_data.append(datum)
            
        if missing_data:
            return {'success': False, 'code': 400, 'message': f'Missing the following in message[{messages.index(message)}]\'s data: {missing_data}'}, 400
        
        if message['sender'] not in ["account1", "account2"]:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. sender must be \'account1\' or \'account2\''}, 400
        
        try:
            float(message['delay'])
        except:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. delay must be float or int'}, 400
        
        if message['response'] not in ["mention", "reply", "neutral"]:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. response must be \'mention\', \'reply\', or \'neutral\''}, 400
        
        if messages.index(message) == 0:
            if message['response'] not in ['mention', 'netural']:
                return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. response must be \'mention\' or \'neutral\''}, 400
 
        if not message['content']:
            return {'success': False, 'code': 400, 'message': f'error in in messages[{messages.index(message)}]. content cannot be empty'}, 400
                
                
        
    db.cmd("INSERT INTO conversations VALUES(%s, %s, %s)", value=(None, request_data['name'], json.dumps(request_data['messages'])))
    
    conversation_id = db.get_value("id", table="conversations", order="id DESC")
    return {'success': True, 'id': conversation_id}



@app.route('/conversations/<int:conversation_id>', methods=["DELETE"])
def delete_conversation(conversation_id):
    db.cmd("DELETE FROM conversations WHERE id=%s", value=(conversation_id,))
    return {'success': True}



@app.route('/status', methods=["GET"])
def get_status():
    return db.get_value("value", table="options", search_filter="name", value=("status",))


@app.route('/status/<new_status>', methods=["GET"])
def change_status(new_status):
    db.cmd("UPDATE options SET value=%s WHERE name=%s", value=(new_status, "status"))
    
    return {'success': True}



app.run('0.0.0.0', 80, False)