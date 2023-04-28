from aiogram.types import *
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from controller import dp, bot, logger
from database import *
from utils import Button
from static import *
from utils import check_user_


@dp.message_handler(commands=['start'])
@check_user_
async def start_(message: Message):
    await message.answer(start, reply_markup=ReplyKeyboardRemove())