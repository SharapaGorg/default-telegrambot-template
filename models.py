from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, nullable=False)
    auth_date = Column(Integer, nullable=False) # timestamp of registration date
    last_seen = Column(String, nullable=False)
    username = Column(String, nullable=True)
    fullname = Column(String, nullable=True)


class Moderator(Base):
    __tablename__ = 'moderators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    level = Column(String, nullable=False)
    date = Column(Integer, nullable=False) # timestamp