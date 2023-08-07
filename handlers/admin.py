from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from dataBase import sqlite_db

from create_bot import dp, storage


class FSMAdmin(StatesGroup):
    photo = State()
    type = State()
    weight = State()
    price_cake = State()
    price_dec = State()
    date = State()
    description = State()


# Start new dialog
# @dp.message_handler(commands='new cake', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('photo')

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.reply('next - type')
    await FSMAdmin.next()


# @dp.message_handler(state=FSMAdmin.name)
async def load_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMAdmin.next()
    await message.reply('next - weight')


# @dp.message_handler(state=FSMAdmin.weight)
async def load_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('next - price')


# @dp.message_handler(state=FSMAdmin.price_cake)
async def load_price_cake(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_cake'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('next - price dec')


# @dp.message_handler(state=FSMAdmin.price_dec)
async def load_price_dec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_dec'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('next - date')


# @dp.message_handler(state=FSMAdmin.date)
async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSMAdmin.next()
    await message.reply('next description')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desciption'] = message.text
    await FSMAdmin.next()
    async with state.proxy() as data:
        await message.reply(str(data))

    await sqlite_db.sql_add_command(state)
    await state.finish()





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['new_cake'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_type, state=FSMAdmin.type)
    dp.register_message_handler(load_weight, state=FSMAdmin.weight)
    dp.register_message_handler(load_price_cake, state=FSMAdmin.price_cake)
    dp.register_message_handler(load_price_dec, state=FSMAdmin.price_dec)
    dp.register_message_handler(load_date, state=FSMAdmin.date)
    dp.register_message_handler(load_description, state=FSMAdmin.description)