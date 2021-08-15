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


class UserData(BASE):
    __tablename__ = "user_data"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    a_count = Column(Integer)
    f_count = Column(Integer)

    def __init__(
        self,
        user_id,
        username,
        a_count,
        f_count,
    ):
        self.user_id = user_id
        self.username = username
        self.a_count = a_count
        self.f_count = f_count

    def to_dict(self):
        dic = {
            "user_id": self.user_id,
            "username": self.username,
            "a_count": self.a_count,
            "f_count": self.f_count,
        }
        return dic


class WebhookData(BASE):
    __tablename__ = "webhook_data"
    webhook_id = Column(Integer, primary_key=True)
    webhook_url = Column(String(200))


class WebhookMapping(BASE):
    __tablename__ = "webhook_mapping"
    user_id = Column(Integer, primary_key=True)
    webhook_id = Column(Integer)


BASE.metadata.create_all(ENGINE)


def get_user_id(username):
    user = SESSION.query(UserData).filter(UserData.username == username).first()
    if user is None:
        user = UserData(username=username)
        SESSION.add(user)
        SESSION.commit()
    return user.user_id


def get_webhook_id(webhook_url):
    webhook = (
        SESSION.query(WebhookData)
        .filter(WebhookData.webhook_url == webhook_url)
        .first()
    )
    if webhook is None:
        webhook = WebhookData(webhook_url=webhook_url)
        SESSION.add(webhook)
        SESSION.commit()
    return webhook.webhook_id


def map_user_webhook(user_id, webhook_id):
    prev_mapping = (
        SESSION.query(WebhookMapping)
        .filter(
            WebhookMapping.webhook_id == webhook_id
            and WebhookMapping.user_id == user_id
        )
        .first()
    )
    if prev_mapping is not None:
        return
    mapping = WebhookMapping(
        user_id=user_id,
        webhook_id=webhook_id,
    )
    SESSION.add(mapping)
    SESSION.commit()


def get_webhook_urls(username):
    return (
        SESSION.query(WebhookData.webhook_url)
        .filter(WebhookData.webhook_id == WebhookMapping.webhook_id)
        .filter(WebhookMapping.webhook_id == UserData.user_id)
        .filter(UserData.username == username)
        .all()
    )


def get_all_users():
    return SESSION.query(UserData).all()
