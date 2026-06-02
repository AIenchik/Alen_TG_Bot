from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import kb1

router = Router()


# /start
@router.message(Command('start'))
async def command_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"""
Привет, {message.chat.first_name}! 👋

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
