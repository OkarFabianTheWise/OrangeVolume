# venv\Scripts\Activate.ps1
from sell import sell_token
from buy import buy_token
from telebot import TeleBot
import telebot, time

BOT_TOKEN = ''
bot = TeleBot(token=BOT_TOKEN)

# volume amount
volume_amount = 0

# Token to run volume on
token = ''

# function to initiate bot
@bot.message_handler(commands=['volume'])
def initiate_volume(message):
    try:
        rep = bot.reply_to(message, "enter amount to run volume (in sol)\nEg: 0.1 , 0.5, 2")
        bot.register_next_step_handler(rep, pre_checks)
    except Exception as x:
        print("initiate_volume:", x)

# validate amount
def instance(value):
    try:
        input_value = float(value)
        return isinstance(input_value, (int, float))
    except Exception as d:
        return False
         
def pre_checks(message):
    try:
        global volume_amount
        value = message.text 
        if instance(value):
            volume_amount = float(value)
            start_volume_loop()
    except Exception as v:
        print("validate_amount:", v)
        
def start_volume_loop():
    try:
        global volume_amount
        buy_token(token, seed, volume_amount)
        # sleep 5 seconds
        time.sleep(5)
        sell_token(token, volume_amount, seed)
        time.sleep(5)
    except Exception as s:
        print("start_volume_loop:", s)
        time.sleep(5)