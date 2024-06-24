from aiogram import F
from aiogram.types import *
from random import randint

from controller import dp

# for some reason without this useless function buttons does not work
@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))