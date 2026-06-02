from aiogram.fsm.state import State, StatesGroup


class GptState(StatesGroup):
    gpt = State()
