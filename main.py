from api import app
from controller import config_parser, bot, dp
from rich import print
import handlers

WEBHOOK_PATH = f'https://c1e2-188-123-230-175.ngrok-free.app'
WEBHOOK_URL = f"{WEBHOOK_PATH}/bot/"

@app.on_event('startup')
async def on_start():
    await bot.set_webhook(url=WEBHOOK_URL + config_parser.token)
    
    dp.include_router(handlers.get_handlers_router())
    print('bot launched')
    
    bot_self = await bot.get_me()
    other_bot_self = await bot.get_me()
    
    print("!!!:", other_bot_self.username)

    print("Bot launch initiated [+]")
    print(f"Username: [bold green]@{bot_self.username}[/bold green]")
    print("Nickname: ", bot_self.full_name) 