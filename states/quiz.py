from aiogram.fsm.state import StatesGroup, State

class QuizState(StatesGroup):
    topic_state = State()
    quiz_state = State()