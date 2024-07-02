import sys

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# from utils.parsers import ConfigParser
import datetime, json, os
from static import *


class ConfigParser:
    def __init__(self):
        path = os.path.join(AIOGRAM_CONFIG)
        if not os.path.exists(path):
            path = os.path.join("..", path)

        if not os.path.exists(path):
            print(
                f"[bold red] Config file does not exists [{AIOGRAM_CONFIG}][\bold red]"
            )
            exit(0)

        with open(path, "r", encoding="utf-8") as read_stream:
            data = read_stream.read()

        try:
            self.data = json.loads(data)
        except:
            print(
                f"[bold red] Config file has critical syntax errors [{AIOGRAM_CONFIG}][\bold red]"
            )
            exit(0)
            return

    @property
    def token(self):
        return self.data["TOKEN"]
    
    @property
    def reserved_token(self):
        return self.data['RESERVED_TOKEN']


config_parser = ConfigParser()

session = AiohttpSession(
    api=TelegramAPIServer.from_base("http://localhost:8080", is_local=True)
)   

bot = Bot(config_parser.token, parse_mode=None)
bot2 = Bot(config_parser.reserved_token, parse_mode=None)

dp = Dispatcher()
dp["started_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


###### DATABASE ######
engine = create_engine("sqlite:///database/base")

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)()
