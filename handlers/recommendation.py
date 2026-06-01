from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from services.chat_gpt import ChatGptService
from states.recommendation import RecommendationState
from prompts.recommendation import recommendation_prompt
from keyboards.prof_keyboard import make_row_keyboard
from keyboards.inline_keyboard import inline_keyboard_recommendation
from keyboards.keyboards import kb1

router = Router()

available_categories = ['Фильмы', 'Книги', 'Музыка']

@router.message(Command('recommend'))
async def recommendation_command(message: types.Message, state: FSMContext):
    await state.clear()
    photo = types.FSInputFile('images/gpt-4o.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Выбери категорию из предложенных ниже!',
        reply_markup=make_row_keyboard(available_categories)
    )
    await state.set_data({'category': '', 'not_liked': [], 'genre': ''})
    await state.set_state(RecommendationState.choose_state)

@router.message(RecommendationState.choose_state, F.text.in_(available_categories))
async def category_choose(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer(f'Хорошо, теперь напиши жанр')
    await state.set_state(RecommendationState.recommendation)

@router.message(RecommendationState.choose_state)
async def incorrect_choose(message: types.Message):
    await message.answer('К сожалению такой темы нет, выбери из предложенных ниже',
                         reply_markup=make_row_keyboard(available_categories))

@router.message(RecommendationState.recommendation)
async def recommendation(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    await state.update_data(genre=message.text)
    await message.answer(f'Сейчас подберу для тебя вариант')
    data = await state.get_data()
    not_liked = data.get('not_liked')
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': recommendation_prompt.get(data.get('category')) + message.text
            },
        ]
    )

    not_liked.append(answer)
    await state.update_data(not_liked=not_liked)
    await message.answer(answer, reply_markup=inline_keyboard_recommendation)

@router.callback_query(F.data == 'not_liked')
async def dont_liked(callback: types.CallbackQuery, state: FSMContext, chat_gpt_service: ChatGptService):
    data = await state.get_data()
    not_liked = data.get('not_liked')
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': recommendation_prompt.get(data.get('category')) + data.get("genre") + f'''
                Не предлагай эти не понравившиеся произведения {not_liked}'''
            },
        ]
    )

    not_liked.append(answer)
    await state.update_data(not_liked=not_liked)
    await callback.message.answer(answer, reply_markup=inline_keyboard_recommendation)
    await callback.answer()

@router.callback_query(F.data == "done")
async def end_translation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"""
    Привет, {callback.from_user.first_name}! 👋

    Я GPT-бот 🤖

    Что умею:
    • генерировать случайные факты
    • отвечать на вопросы
    • могу стать известной личностью
    • можем сыграть в викторину

    Выбери действие ниже 👇
    """,
                                  reply_markup=kb1
                                  )
    await callback.answer()
    await state.clear()