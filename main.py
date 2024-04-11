# from aiogram.utils import executor
# from utils import startupx
from controller import dp, bot
import asyncio


import handlers

# executor.start_polling(dp, skip_updates=True, on_startup=startup)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())