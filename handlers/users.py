from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import *
from controller import bot, dp, logger
from database import *
from static import *
from utils import *


@dp.message_handler(commands=['start'])
@check_user
async def start_(message: Message):
    await message.answer(start, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['ping'])
@check_user
async def ping_(message : Message):
    await message.answer("Pong!")


@dp.message_handler(commands=['button_slider'])
@check_user
async def button_slider_example(message: Message):
    message = await message.answer('What button slider looks like:')

    buttons = list()
    for k in range(25):
        b = Button(f'button number {k}')
        b.onClick(show_button_number, k)

        buttons.append(b)

    button_slider = ButtonSlider(message, buttons, columns=3, rows=4)
    await button_slider.render_page()

async def show_button_number(callback : CallbackQuery, button_number : int):
    await bot.send_message(callback.from_user.id, f"This is a button number : {button_number}")
