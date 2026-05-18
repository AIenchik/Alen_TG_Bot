from aiogram import Router, types
from aiogram.filters.command import Command
from keyboards.keyboards import kb1
from utils.random_fox import fox

router = Router()

# /start
@router.message(Command('start'))
async def command_start(message: types.Message):
    print(message)
    await message.answer(f'Hi, {message.chat.first_name}!', reply_markup=kb1)

# /info
@router.message(Command('info'))
async def command_info(message: types.Message):
    await message.answer('This is GPT bot')

# /fox
@router.message(Command('fox'))
async def command_fox(message: types.Message):
    await message.answer_photo(fox())

async def main():
    await dp.start_polling(bot)



