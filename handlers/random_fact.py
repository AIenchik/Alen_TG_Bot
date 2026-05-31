from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from services.chat_gpt import ChatGptService
from prompts.random_fact import random_fact, random_role
from keyboards.inline_keyboard import inline_keyboard_random
from keyboards.keyboards import kb1
from states import random



router = Router()


used_facts = set()


@router.message(Command('random'))
async def command_random(message: types.Message, chat_gpt_service: ChatGptService, state: FSMContext):
    answer = await chat_gpt_service.ask(role_text=random_role, user_text=random_fact)

    photo = types.FSInputFile('images/random_fact.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Ты в режиме генерации случайных фактов!'
    )
    await state.set_state(random.RandomState.random)
    await message.answer(answer, reply_markup=inline_keyboard_random)
    used_facts.add(answer)




@router.callback_query(F.data == 'want_more')
async def callback_ask_gpt(callback: types.CallbackQuery, chat_gpt_service: ChatGptService):
    answer = await chat_gpt_service.ask(
        role_text=random_role, user_text=random_fact + f'Без вот этих уже выданных фактов {list(used_facts)}'
    )
    await callback.message.answer(answer, reply_markup=inline_keyboard_random)
    await callback.answer()

@router.callback_query(F.data == 'done')
async def callback_ask_gpt(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"""
Привет, {callback.from_user.first_name}! 👋

Я GPT-бот 🤖

Что умею:
• генерировать случайные факты
• отвечать на вопросы
• могу стать известной личностью
• генерировать квиз

Выбери действие ниже 👇
""",
    reply_markup=kb1
)
    await callback.answer()
