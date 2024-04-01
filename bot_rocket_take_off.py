from config import *
from dictionary import TEXTS
import time
import os
import threading
import telebot # Api Telegram
from typing import List, NamedTuple, Text, Optional
from httpx import Client
from datetime import datetime, timedelta
from urllib.parse import quote, urljoin
from telebot.types import InlineKeyboardMarkup # Create buttons
from telebot.types import InlineKeyboardButton # Define buttons
from flask import Flask, request
from waitress import serve


"""
Bot rocket takeoff.

This exercise has two game modes.

The first option
    Question: Has the rocket been launched yet?
    Options:
    🔹 Yes: provides release date.
    🔹 No: keep playing.

The second option
    Question: Does the frame belong to the launch?
    Options:
    🔹 Yes, it belongs: provides release date.
    🔹 No, but the rocket has already taken off: keep playing.
    🔹 No, it hasn't taken off: keep playing.
    
The operation is as follows

Bot
    🔹 Indicates a welcome message.
    🔹 Provides options to choose a language Spanish | English.
    🔹 Provides options to choose the game mode with its respective description.
    🔹 Consume the api and start the game.
    🔹 Provides options for the chosen game mode.
    🔹 Provides an end-of-game message.
    🔹 It always confirms the option selected by the user with a confirmation message.
    🔹 To consume the provided API, the base code is taken as support.

Autor: Michael Arias
"""

bot = telebot.TeleBot(TELEGRAM_TOKEN)
api_base = API_BASE
video_name = VIDEO_NAME

# Texts in English and Spanish
INITIAL_COMMAND = ["start"]
HELP_COMMANDS = ["help", "ayuda"]
TYPES_NOT_ALLOWED = ["text", "audio", "document", "animation", "game", "photo", "sticker",
    "video", "video_note", "voice", "location", "contact", "venue", "dice",
    "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo",
    "delete_chat_photo", "group_chat_created", "supergroup_chat_created",
    "channel_chat_created", "migrate_to_chat_id", "migrate_from_chat_id",
    "pinned_message", "invoice", "successful_payment", "connected_website",
    "poll", "passport_data", "proximity_alert_triggered", "video_chat_scheduled",
    "video_chat_started", "video_chat_ended", "video_chat_participants_invited",
    "web_app_data", "message_auto_delete_timer_changed", "forum_topic_created",
    "forum_topic_closed", "forum_topic_reopened", "forum_topic_edited",
    "general_forum_topic_hidden", "general_forum_topic_unhidden", "write_access_allowed",
    "user_shared", "chat_shared", "story"
]
USERS = {}
DATA_API = {'frames': {'initial': 0, 'half': 0, 'total':0},
            'exception': {
                'message_api': '',
                'message_api_frame': ''
            }      
    }
# Total seconds in the video
FRAME_TO_SEG = 2052
# Approximate video date and time
VIDEO_DATE = datetime(2018, 2, 6, 20, 23, 0)
# Falcon Heavy Test Flight launch date and time
RELEASE_DATE = datetime(2018, 2, 6, 20, 45, 0)
# Falcon Heavy Test Flight launch date and time format
FINAL_RELEASE_DATE = RELEASE_DATE.strftime("%Y-%m-%d %H:%M:%S")

web_server = Flask(__name__)
@web_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
# https://bot-rocket-6690def7c07d.herokuapp.com/


class Video(NamedTuple):
    """
    That's a video from the API
    """
    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text

class APIClient:
    BASE_URL = API_BASE
    def __init__(self):
        self.client = Client(timeout=30)
    def video(self, video: Text) -> Video:
        """
        Fetches information about a video
        """
        try:
            r = self.client.get(urljoin(self.BASE_URL, f"video/{quote(video)}/"))
            r.raise_for_status()
            return Video(**r.json())
        except Exception as e:
            DATA_API['exception']['message_api'] = e
    def video_frame(self, video: Text, frame: int) -> bytes:
        """
        Fetches the JPEG data of a single frame
        """
        try:
            r = self.client.get(urljoin(self.BASE_URL, f'video/{quote(video)}/frame/{quote(f"{frame}")}/'))
            return  r.status_code
        except Exception as e:
            DATA_API['exception']['message_api_frame'] = e

def api_client(option: Text, frame: Optional[int] = 0):
    # Create an APIClient instance
    api_client = APIClient()
    # Get video data
    if option == 'initial':
        video_data = api_client.video(video_name)
        if video_data.frames > 0 and ((DATA_API['frames']['initial'] + 1) < video_data.frames // 2):
            DATA_API['frames']['total'] = video_data.frames
    # Validate request status with frame
    elif option == 'frame':
        frame_response = api_client.video_frame(video_name, frame)
        return frame_response

# Message error Api
def error_api(cid: int,):
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, TEXTS['messages']['errorApi'])
# Comand /Start
@bot.message_handler(commands=INITIAL_COMMAND)
def cod_start_languages(message):
    api_client('initial')
    if not DATA_API['exception']['message_api']:
        bot.send_chat_action(message.chat.id, 'typing')
        initialize_values(message.chat.id)
        markup_start = InlineKeyboardMarkup(row_width = 2) 
        btEN = InlineKeyboardButton(TEXTS['languages']['es']['languages_options']['button_text'], callback_data=TEXTS['languages']['es']['languages_options']['option'])
        btES = InlineKeyboardButton(TEXTS['languages']['en']['languages_options']['button_text'], callback_data=TEXTS['languages']['en']['languages_options']['option'])
        markup_start.add(btEN, btES)
        welcome_message = f"{TEXTS['languages']['es']['languages_options']['welcome']}\n{TEXTS['languages']['en']['languages_options']['welcome']}"
        bot.send_message(message.chat.id, welcome_message, reply_markup=markup_start)
    else:
        error_api(message.chat.id)
# Select game
def select_game(cid: int,):
    bot.send_chat_action(cid, 'typing')
    
    if not DATA_API['exception']['message_api']:
        markup_game = InlineKeyboardMarkup(row_width = 2) 
        game_one = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['option'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['option_selected'])
        game_two = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['option'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['option_selected'])
        markup_game.add(game_one, game_two)
        
        message_select_game = f"{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['mode_game']}\n{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['description']}\n{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['description']}"
        bot.send_message(cid, message_select_game, reply_markup=markup_game)    
    else:
        error_api(cid)

# Responds when you need help
@bot.message_handler(commands=HELP_COMMANDS)
def bot_menssges_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, TEXTS['messages']['help'])

# Responds when they are not commands
@bot.message_handler(content_types=TYPES_NOT_ALLOWED)
def bot_menssges_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, TEXTS['messages']['error'])

# Button response
@bot.callback_query_handler(func=lambda x: True)
def response_buttons(call):
    cid = call.from_user.id
    mid = call.message.id
    bot.send_chat_action(cid, 'typing')
    if not DATA_API['exception']['message_api']:
        # Language buttons
        if call.data == TEXTS['languages']['es']['languages_options']['option'] or call.data == TEXTS['languages']['en']['languages_options']['option']:
            initialize_values(cid)
            bot.delete_message(cid, mid)
            USERS[cid]['finalLanguageOption'] = call.data
            if call.data == TEXTS['languages']['es']['languages_options']['option']:
                bot.send_message(cid, TEXTS['languages']['es']['languages_options']['language_selected'])
            elif call.data == TEXTS['languages']['en']['languages_options']['option']:
                bot.send_message(cid, TEXTS['languages']['en']['languages_options']['language_selected'])
            select_game(cid)
        # Game mode buttons
        elif call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['option_selected'] or call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['option_selected']:
            bot.delete_message(cid, mid)
            USERS[cid]['game_mode'] = call.data
            message_response = f"{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['game_selected']}{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][call.data]['description']}"
            if call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['option_selected']:
                bot.send_message(cid, message_response)
                game_mode_one(cid)
            elif call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['option_selected']:
                bot.send_message(cid, message_response)
                game_mode_two(cid)
        # Game mode buttons one 1
        elif call.data in TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['one']['options']['answer_options'].values():
            bot.delete_message(cid, mid)
            # Select option one
            if call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_options']['one']:
                message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['one']
                bot.send_message(cid, message_response)
                end_game(cid)
            # Select option two
            elif call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_options']['two']:
                message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['two']
                bot.send_message(cid, message_response)
                game_mode_one(cid)
        # Game mode buttons two 2
        elif call.data in TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['two']['options']['answer_options'].values():
            bot.delete_message(cid, mid)
            # Select option one
            if call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_options']['one']:
                message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['one']
                bot.send_message(cid, message_response)
                end_game(cid)
            # Select option two
            elif call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_options']['two']:
                message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['two']
                bot.send_message(cid, message_response)
                game_mode_two(cid, call.data)
            # Select option three
            elif call.data == TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_options']['three']:
                message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['three']
                bot.send_message(cid, message_response)
                game_mode_two(cid, call.data)
            else:
                error_api(cid)
                
# Game mode one  
def game_mode_one(cid: int):
    bot.send_chat_action(cid, 'upload_photo')
    response_logic_game = game_logic()
    if response_logic_game == 'final':
        message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['limit']
        bot.send_message(cid, message_response)
        end_game(cid)
    else:
        api_response = api_client('frame', response_logic_game)
        if api_response == 200:   
            url_frame = f'{API_BASE}video/{VIDEO_NAME}/frame/{response_logic_game}'
            bot.send_photo(cid, url_frame)
            markup_game_one = InlineKeyboardMarkup(row_width = 2)                 
            option_one_game_one = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_text']['one'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_options']['one'])
            option_two_game_one = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['answer_text']['two'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_options']['two'])
            markup_game_one.add(option_one_game_one, option_two_game_one)
            question_title = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['question']
            bot.send_message(cid, question_title, reply_markup=markup_game_one)
        else:
            error_api(cid)

# Game mode two     
def game_mode_two(cid: int, option: Optional[Text] = ''):
    bot.send_chat_action(cid, 'upload_photo')
    response_logic_game = game_logic(option)
    if response_logic_game == 'final':
        message_response = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['limit']
        bot.send_message(cid, message_response)
        end_game(cid)
    else:
        api_response = api_client('frame', response_logic_game)
        if api_response == 200:   
            url_frame = f'{API_BASE}video/{VIDEO_NAME}/frame/{response_logic_game}'
            bot.send_photo(cid, url_frame)
            markup_game_two = InlineKeyboardMarkup(row_width = 1)                 
            option_one_game_two  = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['one'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_options']['one'])
            option_two_game_two  = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['two'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_options']['two'])
            option_three_game_two  = InlineKeyboardButton(TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_text']['three'], callback_data=TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode'] ]['options']['answer_options']['three'])
            markup_game_two.add(option_one_game_two , option_two_game_two , option_three_game_two )
            question_title = TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options'][USERS[cid]['game_mode']]['options']['question']
            bot.send_message(cid, question_title, reply_markup=markup_game_two)
        else:
            error_api(cid)
            
# Game one logic
def game_logic(option: Optional[Text] = ''):
    if DATA_API['frames']['total'] < 1 or (DATA_API['frames']['initial'] + 1 == DATA_API['frames']['total']):
        return 'final'

    if DATA_API['frames']['initial'] + 1 < DATA_API['frames']['total']:
        DATA_API['frames']['half'] = (DATA_API['frames']['initial'] + DATA_API['frames']['total']) // 2
        if option == 'game_two_op_two' or not option:
            DATA_API['frames']['initial'] = DATA_API['frames']['half']
        elif option == 'game_two_op_three':
            DATA_API['frames']['total'] = DATA_API['frames']['half']
        return DATA_API['frames']['half']

# End game 
def end_game(cid: int,):
    selected_frame = frame_to_minute()
    message_response = f"{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['final_answer']}{selected_frame}\n{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['release_date']}{FINAL_RELEASE_DATE}" 
    bot.send_message(cid, message_response)
    if selected_frame >= datetime.strptime(FINAL_RELEASE_DATE, "%Y-%m-%d %H:%M:%S"):
        message_response = f"{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['correct']}\n{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['goodbye']}"
        bot.send_message(cid, message_response)
    elif selected_frame < datetime.strptime(FINAL_RELEASE_DATE, "%Y-%m-%d %H:%M:%S"):
        message_response = f"{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['false']}\n{TEXTS['languages'][USERS[cid]['finalLanguageOption']]['game_options']['titles']['goodbye']}"
        bot.send_message(cid, message_response)
    quit()

# Frame to minute
def frame_to_minute():
    """
        * Rule of 3 is used to convert the frame to seconds of the video.
        * Add the seconds to the start time of the video
    """
    # Selected frame converted to video seconds
    selected_frame_seg = ((DATA_API['frames']['initial'] * FRAME_TO_SEG) / DATA_API['frames']['total'])
    # Add the seconds to the start time of the video
    selected_date = VIDEO_DATE + timedelta(seconds=selected_frame_seg)
    return selected_date

# Initialize values       
def initialize_values(cid: int,):
    USERS[cid] = {}
    USERS[cid]['finalLanguageOption'] = ''
    DATA_API['frames']['initial'] = 0

def polling():
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling()
      
def start_web_server():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"https://{APP}.herokuapp.com/")
    serve(web_server, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
# Main
if __name__ == '__main__':
    print('Iniciando el bot')
    if os.environ.get('DYNO_RAM'):
        #Start web server
        hilo = threading.Thread(name='hilo_web_server', target=start_web_server)
    else:
        hilo = threading.Thread(name='hilo_polling', target=polling)
    hilo.start()
    print('Bot iniciado')