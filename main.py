import asyncio
import logging
from aiogram import Bot, Dispatcher
import config
from handlers import common, message


async def main():
    TG_TOKEN = config.tg_token
    OPENAI_TOKEN = config.openai_token

    # Turn on logging
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(echo.router)

    await dp.start_polling(bot)

asyncio.run(main())

