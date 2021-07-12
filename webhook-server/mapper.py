import database_api as db


def choose_updater(username):
    return 1


def register_webhook(webhook_url, username):
    user_id = db.get_user_id(username)
    webhook_id = db.get_webhook_id(webhook_url)
    db.map_user_webhook(user_id, webhook_id)
    updater_id = choose_updater(username)
    db.map_user_updater(user_id, updater_id)
