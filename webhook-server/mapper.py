from .database_api import (
    get_user_id,
    get_webhook_id,
    map_user_webhook,
    map_user_updater,
    )

def choose_updater(username):
    return 1


def register_webhook(webhook_url, username):
    user_id = get_user_id(username)
    webhook_id = get_webhook_id(webhook_url)
    map_user_webhook(user_id, webhook_id)
    updater_id = choose_updater(username)
    map_user_updater(user_id, updater_id)
