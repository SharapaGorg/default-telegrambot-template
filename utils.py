import functools, time
from aiogram.types import *
import string
import random
from static import commands, access_denied

from controller import bot, dp, logger
from database import *


async def startup(message):
    bot_self = await bot.get_me()
    print(f'Bot launched [@{bot_self.username}]')

    suggesting_commands = [
        BotCommand(command_name, description=command_desc) for command_name, command_desc in commands.items()
    ]

    await bot.set_my_commands(suggesting_commands)

####### USABLE TOOLS #######


class Button(InlineKeyboardButton):
    """ 
    wrapper of callback_query_handlers 
    that allows you to use buttons without creating callback_data 

    [similar to the onClick function in javascript]
    """
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
    """ decorator of check_user function below """
    @functools.wraps(coro)
    async def wrapper(message: Message, *args, **kwargs):
        await check_user(message)
        try:
            return await coro(message, *args, **kwargs)
        except Exception as e:
            logger.error(e)

    return wrapper


def moder_check_(coro):
    """ decorator of moder_check function below """
    @functools.wraps(coro)
    async def wrapper(message: Message, *args, **kwargs):
        if await check_for_moder(message):
            return await coro(message, *args, **kwargs)

    return wrapper


async def check_user(message: Message):
    """ adds new users to database, and updates 'last seen' status of old users"""
    author = message.from_user
    users = get_users(author.id)

    now = int(time.time())
    if not users:
        username = 'NULL' if author.username is None else author.username
        add_user(author.id, now, username, author.full_name)
        return

    edit_user(author.id, now)

    try:
        logger.info(
            f'MSG from [{author.id}] [@{author.username}] [{author.full_name}] - {message.text} {message.caption}')
    except:
        # if user banned bot
        pass


async def check_for_moder(message: Message) -> bool:
    """ check if user (author of message) is moderator """
    author = message.from_user
    moders = get_moders(author.id)

    if not moders:
        await bot.send_message(author.id, access_denied)
        return False

    return True
