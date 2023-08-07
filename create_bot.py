from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import json

storage = MemoryStorage()

with open("config.json", "r") as json_file:
    json_data = json.load(json_file)

token = json_data["bot_token"]

bot = Bot(token)
dp = Dispatcher(bot, storage=storage)