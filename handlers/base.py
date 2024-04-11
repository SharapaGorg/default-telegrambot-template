from aiogram.types import *
from controller import dp
from static import *
from utils import check_user


@dp.message()
@check_user
async def parse_left_messages(message : Message):
    await message.answer(default)
