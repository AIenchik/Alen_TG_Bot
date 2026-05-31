from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_button_want_more_fact = InlineKeyboardButton(text='Хочу еще факт', callback_data='want_more')
inline_button_done = InlineKeyboardButton(text='Закончить', callback_data='done')
inline_button_want_more_question = InlineKeyboardButton(text='Хочу еще вопрос', callback_data='want_more')
inline_button_another_topic = InlineKeyboardButton(text='Другая тема', callback_data='another_topic')


inline_keyboard_random = InlineKeyboardMarkup(inline_keyboard=[[inline_button_want_more_fact,
                                                         inline_button_done]])
inline_keyboard_talk = InlineKeyboardMarkup(inline_keyboard=[[inline_button_done]])

inline_keyboard_quiz = InlineKeyboardMarkup(inline_keyboard=[
    [inline_button_want_more_question],
    [inline_button_another_topic],
    [inline_button_done]
])