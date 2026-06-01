import asyncio
import logging
from aiogram import Bot, Dispatcher
import config
from handlers import talk, echo, career_choice, random_fact, start, chat_gpt, quiz, translator
from services.chat_gpt import ChatGptService



async def main():
    TG_TOKEN = config.tg_token
    OPENAI_TOKEN = config.openai_token

    # Turn on logging
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    chat_gpt_service = ChatGptService(api_key=OPENAI_TOKEN)
    dp['chat_gpt_service'] = chat_gpt_service

    dp.include_router(start.router)
    dp.include_router(chat_gpt.router)
    dp.include_router(career_choice.router)
    dp.include_router(talk.router)
    dp.include_router(random_fact.router)
    dp.include_router(quiz.router)
    dp.include_router(translator.router)
    # dp.include_router(echo.router)

    await dp.start_polling(bot)

asyncio.run(main())

