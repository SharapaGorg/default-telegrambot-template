from aiogram.types import *
from utils import moder_check
from database import *

from controller import dp

@dp.message_handler(commands=['users_stats'])
@moder_check
async def send_users_stats(message : Message):
    users = get_users()
    moders = get_moders()

    result = f'Total {len(users)} users\nOf them, {len(moders)} moderators'

    await message.answer(result)