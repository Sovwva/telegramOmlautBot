from aiogram import types
from aiogram.dispatcher import dispatcher

import logging

import asyncio

from dataBase import sqlite_db

from create_bot import dp, bot

from handlers import client, admin


async def on_startup():
    sqlite_db.sql_start()


    client.register_handlers_client(dp)
    # admin.register_handlers_admin(dp)

    try:
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run( on_startup() )
