from aiogram import types


start_button = types.KeyboardButton(text='/start')
info_button = types.KeyboardButton(text='/info')
fox_button = types.KeyboardButton(text='/fox')
hr_button = types.KeyboardButton(text='/HR')

keyboard_1 = [
    [start_button], [info_button], [fox_button], [hr_button]
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)