import functools
import time

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import *

from controller import bot, dp, logger
from database import *
from static import *


async def startup(message):
    bot_self = await bot.get_me()
    print(f'Bot launched [@{bot_self.username}]')

    suggesting_commands = [
        BotCommand(command_name, description=command_desc) for command_name, command_desc in commands.items()
    ]

    await bot.set_my_commands(suggesting_commands)


def check_user(coro):
    """ decorator of check_user_ function below """

    @functools.wraps(coro)
    async def wrapper(message: Message, *args, **kwargs):
        await check_user_(message)
        try:
            return await coro(message, *args, **kwargs)
        except Exception as e:
            logger.error(e)

    return wrapper


def moder_check(coro):
    """ decorator of moder_check function below """

    @functools.wraps(coro)
    async def wrapper(message: Message, *args, **kwargs):
        if await check_for_moder(message):
            return await coro(message, *args, **kwargs)

    return wrapper


async def check_user_(message: Message):
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
