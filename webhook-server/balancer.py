from . import database_api as db


class LoadBalancer:
    def __init__(self, server):
        self.server = server

    def allocate_user(self, updater_id):
        # Insert algorithm for load balancing
        users = db.get_all_users()
        return users
