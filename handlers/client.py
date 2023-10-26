import json
import logging

import aiogram.exceptions

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
from main import logger
import datetime

from keyboards import kb_client


async def start(message: types.Message):
    # print(message.chat)
    msg_bot_chat_id = await last_message.get_last_message(message.chat.id)
    if msg_bot_chat_id == None:
        msg_bot = await bot.send_message(text=start_text, chat_id=message.chat.id, reply_markup=kb_client)
        await last_message.update_last_message(message.chat.id, msg_bot.message_id)
    else:
        try:
            await bot.edit_message_text(text=start_text, chat_id=message.chat.id, message_id=msg_bot_chat_id, reply_markup=kb_client)
        except aiogram.exceptions.TelegramBadRequest as e:
            if "message to edit not found" in str(e):
                msg_bot = await bot.send_message(text=start_text, chat_id=message.chat.id, reply_markup=kb_client)
                await last_message.update_last_message(msg_bot.id, msg_bot.message_id)
            if "message is not modified" in str(e):
                await bot.delete_message(chat_id=message.chat.id,
                    message_id=await last_message.get_last_message(message.chat.id))
                msg = await bot.send_message(text=start_text, chat_id=message.chat.id, reply_markup=kb_client)
                await last_message.update_last_message(message.chat.id, msg.message_id)
            else:
                with open("config.json", "r") as json_file:
                    json_data = json.load(json_file)
                admin_id = json_data["admin_id"]
                logger.error(msg=e)
                await bot.send_message(text=str(e), chat_id=admin_id)

    await message.delete()

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

async def default(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    try:
        print(await last_message.get_last_message(message.chat.id))
        await bot.edit_message_text(text="Команда не распознана", chat_id=message.chat.id, message_id= await last_message.get_last_message(message.chat.id))
    except aiogram.exceptions.TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await bot.delete_message(chat_id=message.chat.id, message_id= await last_message.get_last_message(message.chat.id))
            msg = await bot.send_message(text="Команда не распознана", chat_id=message.chat.id)
            await last_message.update_last_message(message.chat.id, msg.message_id)
        elif "message to edit not found" in str(e):
            msg = await bot.send_message(text="Команда не распознана", chat_id=message.chat.id)
            await last_message.update_last_message(chat_id=msg.chat.id, message_bot_id=msg.message_id)
        else:
            with open("config.json", "r") as json_file:
                json_data = json.load(json_file)
            admin_id = json_data["admin_id"]
            logger.error(msg=e)
            await bot.send_message(text=str(e), chat_id=admin_id)


def register_handlers_client(dp: Dispatcher):
    pass
    dp.message.register(start, F.text == "/start")
    # dp.register_message_handler(start, commands=['start'])
    # dp.register_message_handler(end, commands=['end'])
    # dp.register_message_handler(karmel, commands=['karmel'])
    # dp.register_message_handler(cakes, commands=['cakes'])
    dp.message.register(default)