from types import coroutine
from aiogram.types import *
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from async_class import AsyncClass
from controller import bot, dp
from widgets import Button
import typing

from utils.keyboard import get_back_button
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def subscription_panel_callback(
    callback: CallbackQuery, state: FSMContext, back_coro: typing.Coroutine
):
    back = get_back_button()
    back.onClick(back_coro, state)

    pay = Button(text="Оплатить 20 ⭐️", pay=True)
    pay.onClick(subscription_payment_process, state, back_coro)

    await callback.message.edit_text(
        "Subscription callback",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[back], [pay]]),
    )

async def subscription_payment_process(callback : CallbackQuery, state : FSMContext, back_coro : typing.Coroutine):
    prices = [LabeledPrice(label="XTR", amount=10)]
    await callback.message.answer_invoice(
        title="TITLE",
        description="Some very interesting description",
        prices=prices,
        provider_token="",
        payload=f"20_stars",
        currency="XTR",
    )