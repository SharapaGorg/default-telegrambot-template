from sqlalchemy import *
from controller import Session, engine
from models import User, Base
import time

def get_users(
    telegram_id : str = None, 
    id : str = None,
    _session = Session) -> list:
    users = select(User)
    
    if telegram_id is not None:
        users = users.where(User.telegram_id == telegram_id)

    if id is not None:
        users = users.where(User.id == id)

    result = list(_session.scalars(users))
    return result

def edit_user(
    id : str,
    last_seen : str
):
    user = get_users(id)[0]

    setattr(user, "last_seen", last_seen)
    Session.commit()

    return user

def add_user(
    telegram_id : str,
    last_seen : str,
    username : str,
    fullname : str
):
    user = User(
        telegram_id = telegram_id,
        last_seen = int(time.time()),
        username = username,
        fullname = fullname,
        auth_date = int(time.time())
    )

    Session.add(user)
    Session.commit()

    return user

def __drop_table():
    User.__table__.drop(engine)
