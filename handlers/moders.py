from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import *
from utils import Button, moder_check
from database import *
import datetime

from controller import dp, bot, logger

@dp.message_handler(commands=['users_stats'])
@moder_check
async def send_users_stats(message : Message):
    users = get_users()
    moders = get_moders()

    result = f'Total {len(users)} users\nOf them, {len(moders)} moderators'

    await message.answer(result)