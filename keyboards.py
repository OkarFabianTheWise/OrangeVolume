import telebot

def start_board():
    markup1 = telebot.types.InlineKeyboardMarkup(row_width=2)
    # create the first set of options and buttons
    options1 = ["Add key for wallet A", "Add key for wallet B", "Start Volume", "Stop Volume", "Help"]
    buttons1 = [telebot.types.InlineKeyboardButton(text=option, callback_data=option) for option in options1]
    
    # Add the Fastrack button separately
    fastrack_button = telebot.types.InlineKeyboardButton(
        text="Dev/Engr",
        url="https://t.me/OrkarFabianThewise"
    )
    
    markup1.add(*buttons1)
    markup1.add(fastrack_button)
    return markup1

def start_board_without_info():
    markup1 = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # create the first set of options and buttons
    options1 = [f"🖼 Gif / Video", "Add Token", "Delete Token", f"Add Emoji", f"Add Minimum", f"Buy Step", "TG LINK", "❌ Close Settings"]
    buttons1 = [telebot.types.InlineKeyboardButton(text=option, callback_data=option) for option in options1]
    
    # Add the Fastrack button separately
    fastrack_button = telebot.types.InlineKeyboardButton(
        text="Fastrack",
        url="https://t.me/solanatrendingFastrackbot"
    )
    
    markup1.add(*buttons1)
    markup1.add(fastrack_button)
    return markup1
