from typing import Dict

from aiogram import types, Bot
from fastapi import APIRouter

from controller import dp

webhook_router = APIRouter()

@webhook_router.post('/bot/{bot_token}')
async def bot_webhook(bot_token : str, update: Dict):
    bot_ = Bot(token=bot_token)
    update = types.Update(**update)
    await dp.feed_update(bot=bot_, update=update)