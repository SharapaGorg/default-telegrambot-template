from rich.progress import Progress
from rich.live import Live
import time


progress = Progress()

with Live(progress) as live_stream:
    task1 = progress.add_task("[red]Loading environment...", total=1000)
    task2 = progress.add_task("[green]Starting bot...", total=1000)
   
    time.sleep(.5)    
    from utils import startup
    progress.update(task1, advance=250)

    time.sleep(.5)    
    import asyncio
    progress.update(task1, advance=250)

    time.sleep(.5)    
    import handlers   
    progress.update(task1, advance=250)
   
    from controller import dp, bot
    progress.update(task1, advance=250)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())