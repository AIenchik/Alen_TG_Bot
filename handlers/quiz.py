from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import json
from services.chat_gpt import ChatGptService
from states.quiz import QuizState
from prompts.quiz import TOPICS
from keyboards.prof_keyboard import make_row_keyboard
from keyboards.inline_keyboard import inline_keyboard_quiz
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
    photo = types.FSInputFile('images/quiz_image.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Выбери тему из предложенных ниже, и мы сыграем в викторину!',
        reply_markup=make_row_keyboard(available_topics)
    )
    await state.set_data({'topic': '', 'score': 0, 'total_questions': 0,
                          'current_question': '', 'used_questions': []})
    await state.set_state(QuizState.topic_state)


@router.message(QuizState.topic_state, F.text.in_(available_topics))
async def topic_choose(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    await state.update_data(topic=message.text)
    await message.answer(f'Ты выбрал тему "{message.text}" загружаю викторину!')
    await state.set_state(QuizState.quiz_state)
    data = await state.get_data()
    used_questions = data.get('used_questions')
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': TOPICS.get(data.get('topic'))
            },
        ]
    )

    used_questions.append(answer)
    await state.update_data(current_question=answer,
                            total_questions=data.get("total_questions") + 1,
                            used_questions=used_questions)
    await message.answer(answer)


@router.message(QuizState.topic_state)
async def incorrect_topic(message: types.Message):
    await message.answer(f'К сожалению такой темы нет, выбери из предложенных',
                         reply_markup=make_row_keyboard(available_topics))


@router.message(QuizState.quiz_state)
async def quiz_game(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    data = await state.get_data()
    answer_on_current = await chat_gpt_service.ask(
        messages=[
            {
                "role": "system",
                "content": """
        Проверь ответ пользователя на вопрос.

        Верни ТОЛЬКО JSON без пояснений.

        Формат ответа:

        {
            "correct": true,
            "explanation": "Краткое объяснение почему не верно или верно"
        }
        """
            },
            {
                "role": "user",
                "content": f"""
        Вопрос: {data.get("current_question")}

        Ответ пользователя: {message.text}
        """
            }
        ])
    result = json.loads(answer_on_current)

    if result['correct']:
        await state.update_data(score=data.get("score") + 1)
        await message.answer(
            f'''Молодец! Счет: {data.get("score") + 1} из {data.get("total_questions")} вопросов. {result['explanation']} Еще вопрос?''',
            reply_markup=inline_keyboard_quiz)
    else:
        await message.answer(
            f'К сожалению не верно. Счет: {data.get("score")} из {data.get("total_questions")}. {result['explanation']} Еще вопрос?',
            reply_markup=inline_keyboard_quiz)


@router.callback_query(F.data == 'want_more_question')
async def one_more_question(callback: types.CallbackQuery, state: FSMContext, chat_gpt_service: ChatGptService):
    data = await state.get_data()
    used_questions = data.get('used_questions')
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': TOPICS.get(data.get('topic')) + f'Не повторяй вопросы {used_questions}'
            },
        ]
    )

    used_questions.append(answer)
    await state.update_data(current_question=answer,
                            total_questions=data.get("total_questions") + 1,
                            used_questions=used_questions)
    await callback.message.answer(answer, reply_markup=inline_keyboard_quiz)
    await callback.answer()


@router.callback_query(F.data == 'another_topic')
async def topic_change(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.topic_state)
    await callback.message.answer("Выбери тему из предложенных ниже",
                                  reply_markup=make_row_keyboard(available_topics))
    await state.update_data(score=0, total_questions=0)
    await callback.answer()


@router.callback_query(F.data == 'done')
async def quiz_complete(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        f'''Ты набрал {data.get("score")} из {data.get("total_questions")}, спасибо за участие!''',
        reply_markup=kb1)
    await callback.answer()
    await state.clear()
