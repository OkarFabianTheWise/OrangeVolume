# venv\Scripts\Activate.ps1
# Environment
from database import Database
from sell import sell_token
from buy import buy_token
from helpers import get_user_balance
from keyboards import *
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters

# solana 
from solders.keypair import Keypair
import base58

import telebot, time, requests, os, uvicorn, asyncio, aiohttp
from environs import Env

env = Env()
env.read_env('.env')
from fastapi_config import app

BOT_TOKEN = 'TELEGRAM BOT KEY'

bot = AsyncTeleBot(token=BOT_TOKEN, state_storage=StateMemoryStorage())

# Token to run volume on
token = env("token_to_trade")
decimals = env("decimals")

# volume amount
volume_amount = 0

# running flag
running = True

class MyStates(StatesGroup):
    volume = State()
    keysa = State()
    keysb = State()


# start running the volume   
async def start_volume_loop(chat_id):
    """
    Run a loop for the buy and sell orders. This function creates volume
    for the token set in the env file
    """

    async with Database() as db:
        res1 = await db.get_keya(chat_id)
        for infoA in res1:
            keya = infoA[0]
            walleta = infoA[1]
            print("keya:", infoA[0])
            print("walleta:", infoA[1])
        
        res2 = await db.get_keyb(chat_id)
        for infoB in res2:
            keyb = infoB[0]
            walletb = infoB[1]
            print("keyb:", infoB[0])
            print("walletb:", infoB[1])

    global volume_amount

    while running == True:
        try:
            # check balance of two wallets: if a == 0 and b == 0:
            # buy a. wait for next round
            # if a > b:
            # sell a . buy b
            # if b > a:
            # sell b . buy a
            a = await get_user_balance(walleta, token)
            b = await get_user_balance(walletb, token)

            if a == 0 and b == 0:
                buy_token(token, keya, volume_amount)
                await asyncio.sleep(5)
            elif a > b:
                # sell a
                for _ in range(3):
                    sell_token(token, a, keya)
                    await asyncio.sleep(5)
                    sell_amount = await get_user_balance(walleta, token)
                    
                    if sell_amount == 0:
                        # it means it has been sold so just break
                        break
                # buy b
                buy_token(token, keyb, volume_amount)
                await asyncio.sleep(5)

            elif b > a:
                # sell b
                for _ in range(3):
                    sell_token(token, b, keyb)
                    await asyncio.sleep(5)
                    sell_amount = await get_user_balance(walletb, token)
                    if sell_amount == 0:
                        # it means it has been sold so just break
                        break

                # buy a
                buy_token(token, keya, volume_amount)
                await asyncio.sleep(5)


            # if there's
            await asyncio.sleep(5)
        except Exception as s:
            print("start_volume_loop:", s)
            await asyncio.sleep(10)

# function to handle the inline keyboard callback
@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call,):
    chat_id = call.message.chat.id
    userid = call.from_user.id
    chat_type = call.message.chat.type
    
    # check if the user has chosen a time for the contest, "Add key for wallet A", "Add key for wallet B"
    if call.data == "Add key for wallet A":
        try:
            if chat_type == 'private': #and userid == :

                # cancel state there is any active session for user
                iscaller = await bot.get_state(userid, chat_id)

                if iscaller != None:
                    await bot.delete_state(userid, chat_id)
                
                await bot.set_state(userid, MyStates.keysa, chat_id)
                await bot.send_message(chat_id, "please input private key for wallet A")
                
            else:
                pass
        except Exception as a:
            print("Add:", a)

    elif call.data == "Add key for wallet B":
        try:
            if chat_type == 'private': #and userid == :

                # cancel state there is any active session for user
                iscaller = await bot.get_state(userid, chat_id)

                if iscaller != None:
                    await bot.delete_state(userid, chat_id)

                await bot.set_state(userid, MyStates.keysb, chat_id)
                await bot.send_message(chat_id, "please input private key for wallet B")
                
            else:
                pass
        except Exception as a:
            print("wallet b:", a)
    
    elif call.data == "Start Volume":
        try:
            if chat_type == 'private':

                # cancel state there is any active session for user
                iscaller = await bot.get_state(userid, chat_id)

                if iscaller != None:
                    await bot.delete_state(userid, chat_id)

                await bot.set_state(userid, MyStates.volume, chat_id)
                await bot.send_message(chat_id, "Enter amount to run volume (in sol)\nEg: 0.1 , 0.5, 2")
                
            else:
                pass
        except Exception as a:
            print("start volume:", a)

    elif call.data == "Stop Volume":
        try:
            if chat_type == 'private':

                # cancel state there is any active session for user
                iscaller = await bot.get_state(userid, chat_id)

                if iscaller != None:
                    await bot.delete_state(userid, chat_id)

                global running
                running = False
                await bot.send_message(chat_id, "volume completed")
                
            else:
                pass
        except Exception as a:
            print("stop volume:", a)

    elif call.data == "Help":
        try:
            if chat_type == 'private':

                # cancel state there is any active session for user
                iscaller = await bot.get_state(userid, chat_id)

                if iscaller != None:
                    await bot.delete_state(userid, chat_id)

                await bot.send_message(chat_id, "1: add wallet key a\n2:add wallet key b\nstart volume.\n\nuse stop volume button to halt volume.")
                
            else:
                pass
        except Exception as a:
            print("stop volume:", a)

@bot.message_handler(state=MyStates.keysa)
async def add_keya_func(message):
    """
    Handle the user's input for key a.
    """
    try:
        key = message.text
        secret=base58.b58decode(key)
        secret_key = secret[:32]
        payer = Keypair.from_seed(secret_key)
        walleta = payer.pubkey()

        # save the key and the wallet
        async with Database() as db:
            await db.add_keya(message.chat.id, key, str(walleta))

        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, 
                               text=f"*Key A Added Successfully*\n",
                               parse_mode="Markdown"
                               )
    except Exception:
        await bot.send_message(message.chat.id, "Invalid input. Please enter a valid privateKey.")

@bot.message_handler(state=MyStates.keysb)
async def add_keyb_func(message):
    """
    Handle the user's input for key b.
    """
    try:
        key = message.text
        secret=base58.b58decode(key)
        secret_key = secret[:32]
        payer = Keypair.from_seed(secret_key)
        walletb = payer.pubkey()

        # save the key and the wallet
        async with Database() as db:
            await db.add_keyb(message.chat.id, key, str(walletb))

        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, 
                               text=f"*Key B Added Successfully*\n",
                               parse_mode="Markdown"
                               )
    except Exception:
        await bot.send_message(message.chat.id, "Invalid input. Please enter a valid privateKey.")

@bot.message_handler(commands=['start'])
async def start_command(message):
    try:
        """
        bring up the keyboard.
        """
        if message.chat.type == 'private':
            await bot.send_message(message.chat.id,
                                   text="DashBoard",
                                   reply_markup=start_board())
    except Exception as d:
        print("start_command:", d)


@bot.message_handler(state=MyStates.volume)
async def pre_checks(message):
    """
    Handle the user's input for volume amount.
    """
    global volume_amount, running

    try:
        value = message.text
        volume_amount = float(value)
        await bot.delete_state(message.from_user.id, message.chat.id)
        running = True
        await bot.send_message(message.chat.id, 
                               text=f"Volume Running | *{running}*\n\n"
                               f"volume amount | *{volume_amount} SOL*\n"
                               f"max sell retry | *3 times*\n\n"
                               f"Click *Stop Volume* button to stop volume",
                               parse_mode="Markdown"
                               )
        asyncio.create_task(long_task(message.chat.id))
    except ValueError:
        await bot.send_message(message.chat.id, "Invalid input. Please enter a valid number.")

async def long_task(chat_id):
    await start_volume_loop(chat_id)

# validate amount
def instance(value):
    try:
        input_value = float(value)
        return isinstance(input_value, (int, float))
    except Exception as d:
        return False

@bot.message_handler(state="*", commands='cancel')
async def cancel_state(message):
    """
    Cancel the current state.
    """
    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)

# Add custom filters
bot.add_custom_filter(asyncio_filters.StateFilter(bot))

@app.post('/' + BOT_TOKEN)
async def getMessage(update: dict):
    update = telebot.types.Update.de_json(update)
    await bot.process_new_updates([update])
    return "", 200

@app.route("/")
async def webhook():
    await bot.remove_webhook()
    await bot.set_webhook(url='NGROK_URL-OR-SERVER-URL/' + BOT_TOKEN)
    return "", 200

async def main():
    config = uvicorn.Config("fastapi_config:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def couple():
    try:
        await asyncio.gather(webhook(), main())
    except Exception as x:
        print("couple err:", x)

if __name__ == '__main__':
    asyncio.run(couple())
