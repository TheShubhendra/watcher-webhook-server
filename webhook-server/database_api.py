from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from sqlalchemy.ext.declarative import declarative_base

from decouple import config

DATABASE_URL = config("DATABASE_URL")


ENGINE = create_engine(DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=ENGINE)
SESSION = scoped_session(session_factory)
BASE = declarative_base()


class UpdaterData(BASE):
    __tablename__ = "updater_data"
    updater_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    def __init__(self, updater_id, username):
        self.updater_id = updater_id
        self.user_id = user_id


class UserData(BASE):
    __tablename__ = "user_data"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    type = Column(String(10))


class WebhookData(BASE):
    __tablename__ = "webhook_data"
    webhook_id = Column(Integer, primary_key=True)
    webhook_url = Column (String(200))


class WebhookMapping(BASE):
    __tablename__ = "webhook_mapping"
    webhook_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)


BASE.metadata.create_all(ENGINE)


def get_user_id(username):
    user = SESSION.query(UserData).filter(UserData.username == username).first()
    if user is None:
        user = UserData(username = username)
        SESSION.add(user)
        SESSION.commit()
    return user.user_id
