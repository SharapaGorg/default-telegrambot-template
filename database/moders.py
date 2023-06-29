from sqlalchemy import *
from controller import Session, engine
from utils.models import Moderator, Base
from database import get_users

def get_moders(telegram_id = None) -> list:
    moders = select(Moderator)

    if telegram_id is not None:
        user = get_users(telegram_id=telegram_id)

        if not user:
            return []

        moders = moders.where(Moderator.user_id == user[0].id)

    result = list(Session.scalars(moders))
    return result

def add_moder(
    user_id : str
):
    moder = Moderator(
        user_id = user_id
    )

    Session.add(moder)
    Session.commit()

    return moder

Base.metadata.create_all(engine)

