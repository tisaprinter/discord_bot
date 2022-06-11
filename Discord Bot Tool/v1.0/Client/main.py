from urllib import request
import PySimpleGUI as sg
import time
import traceback
import random
import string

from variables import *
from helper import *

MAX_ROWS = 20
MAX_COL = 1

status = requests.get("http://protonman2-conversations.karmonxp.com/status").text

print(status)



def show_window2(main_window):
    layout2 = [[sg.Column(
    [
        [sg.Text('Name       ', justification='right')] + [sg.InputText(key='-NAME-', size=(20, 1))] + [sg.Text('      ', justification='right')] + [sg.Text('Channel ID ', justification='right')] + [sg.InputText(key='-CHANNEL-', size=(20, 1))],
        [sg.Text('Account 1 ', justification='right')] + [sg.InputText(key='-AC1-', size=(20, 1))] + [sg.Text('      ', justification='right')] + [sg.Text('Account 2   ', justification='right')] + [sg.InputText(key='-AC2-', size=(20, 1))],
        [sg.Text('')],
        [sg.Column([[sg.Button("Add", size=(10, 1), key="add_btn")]], expand_x=True, element_justification='center')],
    ]
    , pad=((10,10), (10,5)))]]
    window = sg.Window('Window2', layout2, modal=True, finalize=True)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "add_btn":
            if values['-NAME-'] != '' and values['-CHANNEL-'] != '' and values['-AC1-'] != '' and values['-AC2-'] != '':
                try:
                    inputted_data = {
                        'name': values['-NAME-'],
                        'channel_id': values['-CHANNEL-'],
                        'account1_token': values['-AC1-'],
                        'account2_token': values['-AC2-']
                    }
                    response = add_bot_to_list(inputted_data, main_window)
                    if response != False:
                        break
                except Exception as e:
                    # # print(e)
                    traceback.print_exc()
                    sg.popup_error("Error: Something went wrong")
            else:
                sg.popup("Please fill all fields", title="Error")
        
    window.close()

def add_row(window, key, layout):
    # window[key].expand(layout)
    window.extend_layout(window[key], layout)

def show_window3(main_window):
    dropdown_account = ["Account 1", "Account 2"]
    dropdown_action = ["Mention", "Reply", "Neutral"]

    cc = [sg.Column(
            [
                
                # [sg.Input("Bot2", size=(23, 1),)] + [sg.Combo(dropdown_account, default_value=dropdown_account[0])] + [sg.Input("30",size=(5, 1), pad=((15, 0), (1, 1)),)] + [sg.Combo(dropdown_account, default_value=dropdown_action[0], pad=((20, 0), (1, 1)),)],
            ], key="message_column", size=(500, 778), expand_x=True, expand_y=True, pad=(0,0), vertical_scroll_only = True, scrollable=True, )]

    layout3 = [[sg.Column(
        [
            [sg.Column([[sg.Text("Name    ")] + [sg.InputText(key='-NAME-', size=(20, 1))]], expand_x=True)] + [sg.Column([[sg.Button("Add", auto_size_button=False, expand_x=True, key="add_conversation")]],expand_x=True, element_justification='right')],
            [sg.Text('')],
            [sg.Column([[sg.Text("Messages", font = ("Arial", 20), size=(10, 1),)]], expand_x=True, element_justification='center')],
            [sg.Column([[sg.Button("Add message", key="add_message_row", size=(10, 1),)]], expand_x=True, element_justification='center')],
            [sg.Button("Messages", size=(20, 1), pad=((3,0), (1,1)), disabled=True)] + [sg.Button("Sender", size=(9,1), pad=((7, 0), (1, 1)), disabled=True)] + [sg.Button("Delay", pad=((7, 0), (1, 1)), disabled=True)] + [sg.Button("Response", pad=((7, 0), (1, 1)), disabled=True)],
            # [sg.Text("", size=(1,0))],
            cc
        ], expand_x=True, expand_y=True, pad=(0,0),)]]
    window = sg.Window('Window3', layout3, resizable=True, size=(500, 500), modal=True, finalize=True)
    # print(window['message_column'])
    mcl = 0 # message_column_length
    while True:
        event, values = window.read()
        # print("event: ", event)
        # print("values: ", values)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "add_message_row":
            layout = [[sg.Input("Botnew"+str(random.randint(1,10)), key="i1_"+str(mcl), size=(23, 1),)] + [sg.Combo(dropdown_account,key="i2_"+str(mcl), default_value=dropdown_account[0])] + [sg.Input("30",key="i3_"+str(mcl),size=(5, 1), pad=((15, 0), (1, 1)),)] + [sg.Combo(dropdown_action, key="i4_"+str(mcl),default_value=dropdown_action[0], pad=((20, 0), (1, 1)),)],]
            add_row(window, 'message_column', layout)
            # print("before refresh")
            window.refresh()                                # refresh required here
            # print("before content change")
            window['message_column'].contents_changed()
            # print("contents changed")
            time.sleep(0.1)
            window['message_column'].Widget.canvas.yview_moveto(1.0) 
            mcl += 1
        elif event == "add_conversation":
            if values['-NAME-'] != '':
                try:
                    messages = []
                    for i in range(mcl):
                        temp_dict = {}
                        temp_dict['content'] = values['i1_'+str(i)]
                        temp_dict['sender'] = values['i2_'+str(i)].lower().replace(" ", "")
                        temp_dict['delay'] = values['i3_'+str(i)]
                        temp_dict['response'] = values['i4_'+str(i)].lower().replace(" ", "")
                        messages.append(temp_dict)
                    inputted_data = {
                        'name': values['-NAME-'],
                        'messages': messages
                    }
                    # print("\n", messages, "\n")
                    response = add_conversation_to_list(inputted_data, main_window)

                    if response != False:
                        break
                except Exception as e:
                    # # print(e)
                    traceback.print_exc()
                    sg.popup_error("Error: Something went wrong")
            else:
                sg.popup("Please fill all fields", title="Error")
        
    window.close()

sg.popup_quick_message('Hang on for a moment, this will take a bit to create....', auto_close=True, non_blocking=True, font='Default 18')


### Main window

# ------ Make the Table Data ------
bots_data = [
    ["Bot1", "Delete"],
    ["Bot2", "Delete"],
]

coversations_data = [
    ["Coversation1", "Delete"],
    ["Coversation2", "Delete"],
    ["Coversation3", "Delete"],
]
# headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
headings = ["Name", "Action"]

bots_data = generate_bot_list()
coversations_data = generate_conversation_list()
if bots_data == False or coversations_data == False:
    exit()

col1 = sg.Column([
        [sg.Button(f"Turn {'off' if status == 'on' else 'on'}", auto_size_button=False, expand_x=True, key="toggle_bots")],
        [sg.Frame('Bots:', [
            [sg.Column([
                [sg.Button("Add Bots", auto_size_button=True, expand_x=True, key="add_bots")],
                [sg.Table(values=bots_data, 
                    headings=headings,
                    max_col_width=25,
                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='right',
                    num_rows=10,
                    # alternating_row_color='lightyellow',
                    key='bots_table',
                    # selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='Bot Table')]
            ], expand_y=True,expand_x=True,)]
        ], expand_y=True,expand_x=True,)]
    ],pad=(0,0), expand_x=True, expand_y=True)

col2 = sg.Column([
        [sg.Frame('Conversations:', [
            [sg.Column([
                [sg.Button("Add Conversation", auto_size_button=True, expand_x=True, key="add_conversations")],
                [sg.Table(values=coversations_data, 
                    headings=headings,
                    max_col_width=25,
                    auto_size_columns=True,
                    # display_row_numbers=True,
                    justification='left',
                    num_rows=10,
                    # alternating_row_color='lightyellow',
                    key='conversations_table',
                    # selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='Conversation Table')]
            ], expand_y=True,expand_x=True,)]
        ], expand_y=True,expand_x=True,)]
    ],pad=(0,0), expand_x=True, expand_y=True)




# col1 = sg.Column([
#                   [sg.Frame('Bots:', columm_layout,size=(180,200),pad=(0,0))]
#                 ],vertical_alignment="top",)

layout1 = [[col1, col2]],

window1 = sg.Window('Window1', layout1, resizable=True)


while True:
    event1, values1 = window1.read()
    # print("event", event1)
    # print("values", values1)
    if event1 == sg.WIN_CLOSED:
        break
    if event1 == 'add_bots':
        window2 = show_window2(window1)
    if event1 == 'add_conversations':
        window3 = show_window3(window1)
    if event1 == "toggle_bots":
        status = 'on' if status == 'off' else 'off'
        requests.get(F"http://protonman2-conversations.karmonxp.com/status/{status}")
        window1.Element('toggle_bots').update(f"Turn {'off' if status == 'on' else 'on'}")
    
    if isinstance(event1, tuple):
        if event1[2][1] == 1: # That means Delete
            table_key = event1[0]
            data = window1[event1[0]].Values
            try:
                # Delete the bot from server first
                # print(data[event1[2][0]][0])
                data_id_to_delete = str(data[event1[2][0]][0]).split("_")
                # print("data_id_to_delete", data_id_to_delete)
                data_id_to_delete = data_id_to_delete[len(data_id_to_delete)-1]
                # print("data_id_to_delete", data_id_to_delete)
                if event1[0] == 'bots_table':
                    response = delete_bot(data_id_to_delete)
                else:
                    response = delete_conversation(data_id_to_delete)

                # print(response)

                if str(response['success']).lower() == "false":
                    sg.popup("Error: " + str(response['message']))
                else:
                    data.pop(event1[2][0])
                    window1[event1[0]].update(values=data)
            except Exception as e:
                # print(e)
                sg.popup_error(str(e), keep_on_top=True)
            

window1.close()