import aiogram.exceptions

import create_bot

welcome_text = ("Отлично, давай начнём знакомство с программой,"
                "тебе необходимо создать организацию, или войти в неё")

start_text = ("Ты можешь создать организацию, или войти в новую")

create_organization = ("Отлично, давай создадим организацию, введи название"
                       "\n Примечание, название и пароль не может быть \"start\" и \"отмена\" ")

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, callback_query

from aiogram import F

from dataBase import last_message, manager
from create_bot import dp, bot
import datetime

from keyboards import kb_client


# async def start(message: types.Message):
#     msg bot = last_message.get_last_message()
#     msg_bot_id = last_message.get_last_message(message.chat.id)
#     print(msg_bot)
#     msg_client = message
#     try:
#         await msg_client.delete()
#     except:
#         pass
#     try:
#         if last_message.get_last_message(chat_id=message.cha) != start_text:
#             try:
#                 await msg_bot.edit_text(start_text, reply_markup=kb_client)
#             except aiogram.exceptions.TelegramBadRequest:
#                 msg_bot = await message.answer(text=start_text, reply_markup=kb_client)
#     except NameError:
#         msg_bot = await message.answer(text=welcome_text, reply_markup=kb_client)
#         # bot.delete_message()
#         # print(f'{msg.text}, {msg.message_id}')
#         print(message.from_user.id)

@dp.callback_query(lambda c : c.data == 'create')
async def create(message: types.Message):
    global msg_bot
    global msg_client

    try:
        if msg_bot.text != start_text:
            try:
                await msg_bot.edit_text(create_organization)
            except aiogram.exceptions.TelegramBadRequest:
                msg_bot = await message.answer(text=create_organization)
    except NameError:
        msg_bot = await message.answer(text=create_organization, reply_markup=kb_client)
        # bot.delete_message()
        # print(f'{msg.text}, {msg.message_id}')
        print(message.from_user.id)


# # async def karmel(message: types.Message):
# #     await message.answer('карамель - 300 грамм сахар, 180 сливки, 80 маргарина', reply_markup=kb_client)
#
# async def cakes(message: types.Message):
#     await sqlite_db.sql_read(message)
#
#
# async def end(message: types.Message):
#     await message.answer('session ended', reply_markup=ReplyKeyboardRemove())
#
#

# async def echo_send(message: types.Message):
# #     await message.answer('Команда не найдена')
#
# async def cakes(message: types.Message):
#     await sqlite_db.sql_read(message)
#
#

def register_handlers_client(dp: Dispatcher):
    pass
    # dp.message.register(start, F.text == "/start")
    # dp.register_message_handler(start, commands=['start'])
    # dp.register_message_handler(end, commands=['end'])
    # dp.register_message_handler(karmel, commands=['karmel'])
    # dp.register_message_handler(cakes, commands=['cakes'])