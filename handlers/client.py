from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from dataBase import sqlite_db
from create_bot import dp, bot
import datetime

from keyboards import kb_client

from create_bot import dp


# @dp.message_handler()

async def start(message: types.Message):
    await message.answer('start', reply_markup=kb_client)
    print(message.from_user.id)


# async def karmel(message: types.Message):
#     await message.answer('карамель - 300 грамм сахар, 180 сливки, 80 маргарина', reply_markup=kb_client)

async def cakes(message: types.Message):
    await sqlite_db.sql_read(message)


async def end(message: types.Message):
    await message.answer('session ended', reply_markup=ReplyKeyboardRemove())


#
# async def echo_send(message: types.Message):
#     await message.answer('Команда не найдена')

async def cakes(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(end, commands=['end'])
    # dp.register_message_handler(karmel, commands=['karmel'])
    dp.register_message_handler(cakes, commands=['cakes'])