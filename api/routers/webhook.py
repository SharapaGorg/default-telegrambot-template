from typing import Dict

from aiogram import types
from fastapi import APIRouter

from controller import dp, bot, config_parser

webhook_router = APIRouter()

@webhook_router.post(f'/bot/{config_parser.token}')
async def bot_webhook(update: Dict):
    update = types.Update(**update)
    await dp.feed_update(bot=bot, update=update)