from aiogram.fsm.state import State, StatesGroup


class TranslatorState(StatesGroup):
    choose_language = State()
    translate = State()
