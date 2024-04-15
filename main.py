from controller import dp, bot
from utils import startup
import asyncio


import handlers

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())