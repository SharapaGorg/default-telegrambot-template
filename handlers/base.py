from aiogram.types import *
from controller import dp
from utils import check_user_
from static import texts

@dp.message_handler()
@check_user_
async def parse_left_messages(message : Message):
    await message.answer(texts.default)