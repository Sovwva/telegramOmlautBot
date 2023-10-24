from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

b1 = InlineKeyboardButton(text='Создать организацию', callback_data='create')
b2 = InlineKeyboardButton(text='Войти в организацию', callback_data='end')
# b2 = inline_keyboard.InlineKeyboardButton('/new_cake')
kb_client = InlineKeyboardMarkup(inline_keyboard=[ [ b1 ], [ b2 ] ])