from aiogram.fsm.state import State, StatesGroup


class TalkState(StatesGroup):
    choice = State()
    talk = State()