# pylint: disable=unused-var
import os
import json
import emoji
#from database import Database
import time
import telebot
from time import sleep
from threading import Thread
from telebot import TeleBot
from telebot import TeleBot
from environs import Env
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from utils import to_sol_string
from DatabaseDb import find_pair_by_ca, get_name, get_symbol, get_price, get_sol_price
from repmessages import bot_responses
from flask import Flask, request
app = Flask(__name__)
env = Env()
env.read_env('.env')
BOT_TOKEN = env("BOT_TOKEN")
bot = TeleBot(token=env("BOT_TOKEN"))
client = Client("https://api.mainnet-beta.solana.com")
token_listener_threads = set()
print(client.is_connected())
#db = Database()