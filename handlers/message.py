from aiogram import Router, types, F

router = Router()


@router.message(F.text)
async def echo(message: types.Message):
    if message.text == '/stop':
        await message.answer('Bot is stopped')
    elif 'stop' in message.text:
        await message.answer('Do you wanna to stop the bot?')
    else:
        await message.answer(message.text)