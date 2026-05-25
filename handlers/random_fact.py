from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from services.chat_gpt import ChatGptService
from prompts.random_fact import random_fact, random_role
from keyboards.inline_keyboard import inline_keyboard_random
from keyboards.keyboards import kb1


router = Router()


used_facts = set()


@router.message(Command('random'))
async def command_random(messages: types.Message, chat_gpt_service: ChatGptService):
    answer = await chat_gpt_service.ask(role_text=random_role, user_text=random_fact)

    photo = FSInputFile('images/random_fact.jpg')

    await messages.answer_photo(
        photo=photo,
        caption=answer,
        reply_markup=inline_keyboard_random
    )
    used_facts.add(answer)


@router.callback_query(F.data == 'want_more')
async def callback_ask_gpt(callback: types.CallbackQuery, chat_gpt_service: ChatGptService):
    answer = await chat_gpt_service.ask(
        role_text=random_role, user_text=random_fact + f'Без вот этих уже выданных фактов {list(used_facts)}'
    )
    await callback.message.answer(answer, reply_markup=inline_keyboard_random)
    await callback.answer()

@router.callback_query(F.data == 'done')
async def callback_ask_gpt(callback: types.CallbackQuery):
    await callback.message.answer(f'Тебя приветствует тг бот с подключением GPT', reply_markup=kb1)
    await callback.answer()