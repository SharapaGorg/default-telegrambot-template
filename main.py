from api import app
from controller import config_parser, bot, dp, bot2
from rich import print
import handlers

WEBHOOK_PATH = f'https://0bd6-89-232-118-133.ngrok-free.app'
WEBHOOK_URL = f"{WEBHOOK_PATH}/bot/"

@app.on_event('startup')
async def on_start():
    await bot.set_webhook(url=WEBHOOK_URL + config_parser.token)
    await bot2.set_webhook(url=WEBHOOK_URL + config_parser.reserved_token)
    
    dp.include_router(handlers.get_handlers_router())
    print('bot launched')
    
    bot_self = await bot.get_me()
    other_bot_self = await bot.get_me()
    
    print("!!!:", other_bot_self.username)

    print("Bot launch initiated [+]")
    print(f"Username: [bold green]@{bot_self.username}[/bold green]")
    print("Nickname: ", bot_self.full_name) 

# from rich.progress import Progress
# from rich.live import Live
# from rich import print
# import time
# from random import randint
# from api import app


# progress = Progress()

# def fake_delay():
#     time.sleep(randint(1, 10) / 10) 

# with Live(progress) as live_stream:
#     task1 = progress.add_task("[yellow]Loading environment...", total=1000)
   
#     fake_delay()
#     # from utils import startup
#     progress.update(task1, advance=250)

#     fake_delay()
#     import asyncio
#     progress.update(task1, advance=250)

#     fake_delay()
#     import handlers   
#     progress.update(task1, advance=250)
    
#     fake_delay()
#     from controller import dp, bot
#     progress.update(task1, advance=250)

    



# async def main():
#     await bot.delete_webhook(drop_pending_updates=True)
#     # dp.startup.register(startup)
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     print('[green]Starting bot...')
#     asyncio.run(main())