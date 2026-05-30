from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command('quiz'))
async def quiz_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('This is quiz mod')
