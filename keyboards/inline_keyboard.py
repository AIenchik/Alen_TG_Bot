from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_button_want_more = InlineKeyboardButton(text='Хочу еще факт', callback_data='want_more')
inline_button_done = InlineKeyboardButton(text='Закончить', callback_data='done')

inline_keyboard_random = InlineKeyboardMarkup(inline_keyboard=[[inline_button_want_more,
                                                         inline_button_done]])