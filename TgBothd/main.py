import asyncio
from aiogram import Bot, Dispatcher

from utils.handlers import start_router
from database.models import async_main


async def main():
    await async_main()
    bot = Bot(token='')
    dp = Dispatcher()
    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
