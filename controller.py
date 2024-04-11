import sys

from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime

from config import TOKEN, RESERVE_TOKEN


# clue : https://github.com/MasterGroosha/aiogram-3-guide/blob/master/code/01_quickstart/bot.py
###### APP ######
bot = Bot(RESERVE_TOKEN if sys.platform == 'win32' else TOKEN, parse_mode=None)
dp = Dispatcher()
dp["started_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")



###### DATABASE ######
engine = create_engine("sqlite:///database/base")

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)()
