from aiogram import types


start_button = types.KeyboardButton(text='/start')
info_button = types.KeyboardButton(text='/info')
random_button = types.KeyboardButton(text='/random')
gpt_button = types.KeyboardButton(text='/gpt')
quiz_button = types.KeyboardButton(text='/quiz')
talk_button = types.KeyboardButton(text='/talk')


keyboard_1 = [
    [start_button], [random_button], [gpt_button], [talk_button], [quiz_button]
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)