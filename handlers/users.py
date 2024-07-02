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

router = Router(name="users_router")


@router.message(Command("start"))
@check_user
async def start_(message: Message):
    await message.answer(start, reply_markup=ReplyKeyboardRemove())


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


@router.message(Command("quests"))
@check_user
async def quests_chain_widget_example(message: Message, state: FSMContext):
    user_id = message.from_user.id
    temp = randint(1, 100)

    questions = {
        "name": "What is your name?",
        "surname": "What is your surname?",
        "smart": "Are you a smart person?",
    }
    print(temp)

    async def get_answers(answers: dict):
        print(temp)
        for answer in answers:
            print(answer, answers[answer])

        await bot.send_message(user_id, "Thanks for your answers!")

    chain = await QuestionsChain(user_id, questions, get_answers, state)

    await chain.activate()
