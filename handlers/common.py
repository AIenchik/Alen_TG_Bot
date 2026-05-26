from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import kb1
from utils.random_fox import fox
from states.start import StartState

router = Router()


# /info
@router.message(Command('info'))
async def command_info(message: types.Message):
    await message.answer('This is GPT bot', reply_markup=kb1)

# /fox
@router.message(Command('fox'))
async def command_fox(message: types.Message):
    await message.answer_photo(fox())




