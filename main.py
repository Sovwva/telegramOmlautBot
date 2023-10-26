import aiogram.exceptions
from aiogram import types
from aiogram.dispatcher import dispatcher

import logging

import asyncio

from dataBase import manager
from dataBase import last_message

from create_bot import dp, bot

from handlers import client, admin


async def on_startup():
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
                await last_message.update_last_message(chat_id=chat_id, message_bot_id=msg.message_id)

            client.register_handlers_client(dp)
            await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

    try:
        await skip_updates()
    finally:
        await bot.session.close()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
print(logger.handlers)

if __name__ == "__main__":
    asyncio.run(on_startup())

