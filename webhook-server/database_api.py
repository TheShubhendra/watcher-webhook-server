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


def get_webhook_id(webhook_url):
    webhook = SESSION.query(WebhookData).filter(WebhookData.webhook_url == webhook_url).first()
    if webhook is None:
        webhook = WebhookData(webhook_url=webhook_url)
        SESSION.add(webhook)
        SESSION.commit()
    return webhook.webhook_id


def map_user_webhook(user_id, webhook_id):
    prev_mapping = SESSION.query(WebhookMapping).filter(WebhookMapping.webhook_id == webhook_id and WebhookMapping.user_id == user_id).first()
    if prev_mapping is not None:
        return
    mapping = WebhookMapping(
        user_id=user_id,
    webhook_id=webhook_id,
    )
    SESSION.add(mapping)
    SESSION.commit()


def map_user_updater(user_id, updater_id):
    prev_mapping = SESSION.query(UpdaterData).filter(UpdaterData.user_id == user_id).all()
    if prev_mapping is not None:
       [SESSION.delete(i) for i in prev_mapping]
       SESSION.commit()
    updater = UpdaterData(
        user_id=user_id,
    updater_id=updater_id,
    )
    SESSION.add(updater)
    SESSION.commit()
