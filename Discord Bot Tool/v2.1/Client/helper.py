import base64
import io
# from PIL import Image
import PySimpleGUI as sg

from variables import *
from api_handler import *

DELETE_EMOJI = "🗑️"

# def get_img_data(f, maxsize=(1024, 768), first=True):
#     """Generate image data using PIL
#     """
#     try:
#         img = Image.open(f)
#         img.thumbnail(maxsize)
#         if first:                     # tkinter is inactive the first time
#             bio = io.BytesIO()
#             img.save(bio, format="PNG")
#             del img
#             return bio.getvalue()
#         return ImageTk.PhotoImage(img)
#     except Exception as e:
#         # img = Image.open(joinpath('loading.gif'))
#         img = Image.open(joinpath(f))
#         img.thumbnail(maxsize)
#         if first:                     # tkinter is inactive the first time
#             bio = io.BytesIO()
#             img.save(bio, format="gif")
#             del img
#             return bio.getvalue()
#         return ImageTk.PhotoImage(img)

def add_bot_to_list(inputted_data, window):
    name = inputted_data['name']
    account1_token = inputted_data['account1_token']
    account2_token = inputted_data['account2_token']
    channel_id = inputted_data['channel_id']

    server_data = post_bots(name, account1_token, account2_token, channel_id)
    # server_data = {
    #                 "id": "2",
    #                 "success": "True"
    #             }
    # print("add_bot-server_data:", server_data)
    if str(server_data['success']) == 'True':
        id = server_data['id']
        data = window['bots_table'].Values
        data.append([name+"_"+str(id), DELETE_EMOJI])
        window['bots_table'].update(values=data)
    else:
        # print(server_data['message'])
        sg.popup_error(server_data['message'])
        return False

def add_conversation_to_list(inputted_data, window):
    name = inputted_data['name']
    messages = inputted_data['messages']

    server_data = post_conversations(name, messages)
    # # print(server_data)
    if str(server_data['success']) == 'True':
        id = server_data['id']
        data = window['conversations_table'].Values
        data.append([name+"_"+str(id), DELETE_EMOJI])
        window['conversations_table'].update(values=data)
    else:
        # print(server_data['message'])
        sg.popup_error(server_data['message'])
        return False

def generate_bot_list():
    response = get_bots()
    if str(response['success']) == 'True':
        bots = response['data']
        bot_list = []
        for bot in response['data']:
            id = bot
            name = bot
            bot_list.append([name, DELETE_EMOJI])
        return bot_list
    else:
        # print(response['message'])
        sg.popup_error("Error getting bot list.\n" + str(response['message']))
        return False

def generate_conversation_list():
    response = get_conversations()
    if str(response['success']) == 'True':
        conv_list = []
        for conv in response['data']:
            id = conv['id']
            name = conv['name']
            conv_list.append([name+"_"+str(id), DELETE_EMOJI])
        return conv_list
    else:
        # print(response['message'])
        sg.popup_error("Error getting conversation list.\n" + str(response['message']))
        return False