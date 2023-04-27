import functools, time
from aiogram.types import *
import string, random
import asyncio

from controller import bot, dp, logger
from database import *

async def startup(message):
    bot_self = await bot.get_me()
    print(f'Bot launched [@{bot_self.username}]')

    suggesting_commands = [
        BotCommand("/request", description="Сделать заказ"),
        BotCommand("/account", description="Настройки аккаунта"),
    ]

    await bot.set_my_commands(suggesting_commands)

####### USABLE TOOLS #######

class Button(InlineKeyboardButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(32))

    def onClick(self, coro, *args, **kwargs):
        try:
            @dp.callback_query_handler(lambda call: call.data == self.callback_data)
            async def some_coro(call):
                return await coro(call, *args, **kwargs)

        except Exception as e:
            logger.error(f'{coro} - handler exception --> {e}')

def check_user_(coro):
    @functools.wraps(coro)
    async def wrapper(message : Message, *args, **kwargs):
        await check_user(message)
        try:
            return await coro(message, *args, **kwargs)
        except Exception as e:
            logger.error(e)
        
    return wrapper

def moder_check_(coro):
    @functools.wraps(coro)
    async def wrapper(message : Message, *args, **kwargs):
        if await check_for_moder(message):
            return await coro(message, *args, **kwargs)

    return wrapper

async def check_user(message : Message):
    author = message.from_user
    users = get_users(author.id)

    now = int(time.time())
    if not users:
        username = 'NULL' if author.username is None else author.username
        add_user(author.id, now, username, author.full_name)
        return

    edit_user(author.id, now)

    try:
        logger.info(f'MSG from [{author.id}] [@{author.username}] [{author.full_name}] - {message.text} {message.caption}')
    except:
        pass

async def check_for_moder(message : Message) -> bool:
    author = message.from_user
    moders = get_moders(author.id)

    if not moders:
        await bot.send_message(author.id, "В доступе отказано")
        return False

    return True
    