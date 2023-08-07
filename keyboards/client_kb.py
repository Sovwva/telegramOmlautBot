from aiogram.types import InlineKeyboardButton, inline_keyboard, reply_keyboard, ReplyKeyboardMarkup

b1 = inline_keyboard.InlineKeyboardButton('/start')
b2 = inline_keyboard.InlineKeyboardButton('/new_cake')
b3 = inline_keyboard.InlineKeyboardButton('/end')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row (b1, b2, b3)