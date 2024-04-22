from rich.progress import Progress
from rich.live import Live
from rich import print
import time
from random import randint


progress = Progress()

def fake_delay():
    time.sleep(randint(1, 10) / 10) 

with Live(progress) as live_stream:
    task1 = progress.add_task("[yellow]Loading environment...", total=1000)
   
    fake_delay()
    from utils import startup
    progress.update(task1, advance=250)

    fake_delay()
    import asyncio
    progress.update(task1, advance=250)

    fake_delay()
    import handlers   
    progress.update(task1, advance=250)
    
    fake_delay()
    from controller import dp, bot
    progress.update(task1, advance=250)

    



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('[green]Starting bot...')
    asyncio.run(main())