from aiogram import types


start_button = types.KeyboardButton(text='/start')
info_button = types.KeyboardButton(text='/info')
random_button = types.KeyboardButton(text='/random')
gpt_button = types.KeyboardButton(text='/gpt')
quiz_button = types.KeyboardButton(text='/quiz')
talk_button = types.KeyboardButton(text='/talk')
translator_button = types.KeyboardButton(text='/translate')
recommendation_button = types.KeyboardButton(text='/recommend')


keyboard_1 = [
    [start_button], [random_button], [gpt_button], [talk_button], [quiz_button], [translator_button],
    [recommendation_button]
]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)