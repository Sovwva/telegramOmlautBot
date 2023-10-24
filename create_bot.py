from aiogram import Bot, Dispatcher

import json

with open("config.json", "r") as json_file:
    json_data = json.load(json_file)

token = json_data["bot_token"]

bot = Bot(token)
dp = Dispatcher()