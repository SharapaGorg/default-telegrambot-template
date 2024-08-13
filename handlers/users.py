from aiogram.types import *
from controller import bot, dp
from database import *
from static import *
from utils import *
from widgets import *
import datetime
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from random import randint
from aiogram import Router

from .panels.subscription import *

router = Router(name="users_router")


@router.message(Command("start"))
@check_user
async def start_(message: Message | CallbackQuery, state: FSMContext):
    payment_button = Button(text="Subscription ⭐️")
    payment_button.onClick(subscription_panel_callback, state, start_)

    prefix = (
        message.message.edit_text
        if isinstance(message, CallbackQuery)
        else message.answer
    )

    await prefix(
        start, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[payment_button]])
    )


@router.message(Command("ping"))
@check_user
async def ping_(message: Message, state: FSMContext):
    some_button = Button(text="Click me")
    some_button.onClick(ping_button_click, state)

    markup = InlineKeyboardMarkup(inline_keyboard=[[some_button]])

    await message.answer("Pong!", reply_markup=markup)


async def ping_button_click(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        "PONG PONG !!!", callback.from_user.id, callback.message.message_id
    )


@router.message(Command("button_slider"))
@check_user
async def button_slider_example(message: Message):
    message = await message.answer("What button slider looks like:")

    buttons = list()
    for k in range(25):
        b = Button(text=f"button number {k}")
        buttons.append(b)

        b.onClick(show_button_number, k)

    button_slider = ButtonSlider(message, buttons, columns=3, rows=4)
    await button_slider.render_page()


async def show_button_number(callback: CallbackQuery, button_number: int):
    await bot.send_message(
        callback.from_user.id, f"This is a button number : {button_number}"
    )


@router.message(Command("calendar"))
@check_user
async def calendar_widget_example(message: Message):
    message = await message.answer("What calendar widget looks like:")

    async def date_click_action(date: datetime.date):
        await message.answer(f"User has chosen this date: {date.isoformat()}")

    calendar = Calendar(message, date_click_action)
    await calendar.render_page()


@router.message()
@check_user
async def parse_left_messages(message: Message):
    await message.answer(default)
