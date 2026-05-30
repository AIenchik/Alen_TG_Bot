from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import message_auto_delete_timer_changed
from openai.types.shared_params import response_format_json_object

from services.chat_gpt import ChatGptService
from states.quiz import QuizState
from prompts.quiz import TOPICS
from keyboards.prof_keyboard import make_row_keyboard
from keyboards.inline_keyboard import inline_keyboard_talk
from keyboards.keyboards import kb1

router = Router()

available_topics = [
    'Животные',
    'Игры',
    'Школьные вопросы',
    'Еда'
]

@router.message(Command('quiz'))
async def quiz_command(message: types.Message, state: FSMContext):
    await state.clear()
    photo = types.FSInputFile('images/gpt-4o.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Выбери тему из предложенных ниже, и мы сыграем в квиз!',
        reply_markup=make_row_keyboard(available_topics)
    )
    await state.set_data({'topic': '', 'score': 0, 'previous_messages': []})
    await state.set_state(QuizState.topic_state)

@router.message(QuizState.topic_state, F.text.in_(available_topics))
async def topic_choose(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    await state.update_data(topic=message.text)
    await message.answer(f'Ты выбрал тему "{message.text}" загружаю квиз!')
    await state.set_state(QuizState.quiz_state)

@router.message(QuizState.topic_state)
async def incorrect_topic(message: types.Message):
    await message.answer(f'К сожалению такой темы нет, выбери из предложенных',
                         reply_markup=make_row_keyboard(available_topics))

@router.message(QuizState.quiz_state)
async def quiz_game(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    data = await state.get_data()
    await message.answer(f"Тема: {data.get('topic')}")