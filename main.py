import aiogram.exceptions
from aiogram import types
from aiogram.dispatcher import dispatcher

import requests

import logging

import asyncio

from dataBase import manager
from dataBase import last_message

from create_bot import dp, bot

from handlers import client, admin

# resumption_messages = {}


async def on_startup():
    # manager.create_organization(manager, 1, "lola", "lola")
    # admin.register_handlers_admin(dp)

    # async def send_resumption_message(chat_id):
    #     if chat_id not in resumption_messages:
    #         message = await bot.send_message(chat_id, 'Сообщение о возобновлении работы бота')
    #         resumption_messages[chat_id] = message.message_id
    #
    # async def skip_update():
    #     updates = await bot.get_updates()
    #     chat_ids = {update.message.chat.id for update in updates if update.message.chat.type == 'private'}
    #
    #     for chat_id in chat_ids:
    #         await send_resumption_message(chat_id)  # Отправляем сообщение о возобновлении
    #
    #         # Удаляем все сообщения, кроме сообщения о возобновлении
    #         for update in updates:
    #             if update.message.chat.id == chat_id and update.message.message_id != resumption_messages.get(chat_id):
    #                 await bot.delete_message(chat_id, update.message.message_id)

    async def skip_updates():
        chat_ids = set()
        for update in await bot.get_updates():
            chat_id= update.message.chat.id
            chat_ids.add(chat_id)
            message_id = update.message.message_id
            try:
                await bot.delete_message(chat_id, message_id)
            except aiogram.exceptions.TelegramBadRequest:
                print(chat_id, message_id)
        else:
            try:
                offset = update.update_id
            except:
                pass
            for chat_id in chat_ids:
                try:
                    await bot.delete_message(chat_id, last_message.get_last_message(chat_id))
                except Exception as e:
                    print(e)
                print(offset)
                await bot.get_updates(offset+1)
                msg = await bot.send_message(chat_id, "Работа бота возобновлена")
                last_message.update_last_message(chat_id=chat_id, message_bot_id=msg.message_id, text=msg.text)

            client.register_handlers_client(dp)
            # await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

    try:
        logging.basicConfig(level=logging.INFO)
        await skip_updates()

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(on_startup())
