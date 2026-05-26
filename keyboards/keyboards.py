from aiogram import types


start_button = types.KeyboardButton(text='/start')
info_button = types.KeyboardButton(text='/info')
random_button = types.KeyboardButton(text='/random')
gpt_button = types.KeyboardButton(text='/gpt')


keyboard_1 = [
    [start_button], [info_button], [random_button], [gpt_button]
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)