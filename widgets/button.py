from aiogram.types import *
from aiogram import F
from controller import bot, dp
from utils import logger
import string
import random


class Button(InlineKeyboardButton):
    """
    wrapper of callback_query_handlers
    that allows you to use buttons without creating callback_data

    [similar to onClick function in javascript]

    text: str
    url: str
    login_url: LoginUrl
    pay: bool
    web_app: WebAppInfo

    """


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(32)
        )

    def onClick(self, coro, *args, **kwargs):
        try:
            @dp.callback_query(F.data == self.callback_data)
            async def some_coro(call: CallbackQuery):
                return await coro(call, *args, **kwargs)

        except Exception as e:
            logger.error(f"{coro} - handler exception --> {e}")