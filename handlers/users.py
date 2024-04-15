from aiogram.types import *
from controller import bot, dp
from database import *
from static import *
from utils import *
from widgets import *
import datetime
from aiogram.filters.command import Command

@dp.message(Command('start'))
@check_user
async def start_(message: Message):
    await message.answer(start, reply_markup=ReplyKeyboardRemove())


@dp.message(Command('ping'))
@check_user
async def ping_(message: Message):
    await message.answer("Pong!")


@dp.message(Command('button_slider'))
@check_user
async def button_slider_example(message: Message):
    message = await message.answer('What button slider looks like:')

    buttons = list()
    for k in range(25):
        b = Button(text=f'button number {k}')
        b.onClick(show_button_number, k)

        buttons.append(b)

    button_slider = ButtonSlider(message, buttons, columns=3, rows=4)
    await button_slider.render_page()


async def show_button_number(callback: CallbackQuery, button_number: int):
    await bot.send_message(callback.from_user.id, f"This is a button number : {button_number}")


@dp.message(Command('calendar'))
@check_user
async def calendar_widget_example(message: Message):
    message = await message.answer('What calendar widget looks like:')

    async def date_click_action(date: datetime.date):
        await message.answer(f"User has chosen this date: {date.isoformat()}")

    calendar = Calendar(message, date_click_action)
    await calendar.render_page()


@dp.message(Command('quests'))
@check_user
async def quests_chain_widget_example(message: Message):
    user_id = message.from_user.id

    async def get_answers(answers: dict):
        for answer in answers:
            print(answer, answers[answer])

        await bot.send_message(user_id, "Thanks for your answers!")

    questions = {'name': 'What is your name?',
                 'surname': 'What is your surname?',
                 'smart': 'Are you a smart person?'}

    chain = await QuestionsChain(user_id, questions, get_answers)

    # you can define chain object and activate it whenever you want

    await chain.activate()
