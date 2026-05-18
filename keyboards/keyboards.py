from aiogram import types


start_button = types.KeyboardButton(text='/start')
info_button = types.KeyboardButton(text='/info')
fox_button = types.KeyboardButton(text='/fox')

keyboard_1 = [[start_button], [info_button], [fox_button]]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)