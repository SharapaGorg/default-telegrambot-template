from . import weird
from . import users
from . import moders

from aiogram import Router

def get_handlers_router():
    handlers_router = Router()

    handlers_router.include_router(users.router)
    
    return handlers_router