from aiogram import Router, types, F
from services.chat_gpt import ChatGptService

router = Router()


@router.message(F.text)
async def echo(message: types.Message, chat_gpt_service: ChatGptService):
    if message.text == '/stop':
        await message.answer('Bot is stopped')
    elif 'stop' in message.text:
        await message.answer('Do you wanna stop the bot?')
    else:
        role_text = '''Ты эксперт HR и помощник в телеграмм боте. 
        Отвечай на русском языке. 
        Если вопрос по вакансии it то объясняй подробно для новичков.'''
        answer = await chat_gpt_service.ask(user_text=message.text,
                                            role_text=role_text)
        await message.answer(answer)