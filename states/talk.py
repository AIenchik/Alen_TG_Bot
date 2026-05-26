from aiogram.fsm.state import State, StatesGroup


class TalkState(StatesGroup):
    gpt = State()