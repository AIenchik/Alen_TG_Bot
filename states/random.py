from aiogram.fsm.state import State, StatesGroup


class RandomState(StatesGroup):
    random = State()