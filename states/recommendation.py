from aiogram.fsm.state import State, StatesGroup


class RecommendationState(StatesGroup):
    choose_state = State()
    recommendation = State()