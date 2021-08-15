import asyncio
from .network import NetworkInterface
from .balancer import LoadBalancer
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)


class Updater:
    def __init__(self, id, url):
        self.id = id
        self.url = url


class Server:
    def __init__(self, port):
        self.network = NetworkInterface(self, port)
        self.balancer = LoadBalancer(self)
        self.updaters = []

    def register_updater(self, url):
        updater_id = len(self.updaters)
        self.updaters.append(Updater(updater_id, url))
        return updater_id


server = Server(5000)
loop = asyncio.get_event_loop()
loop.create_task(server.network.serve())
loop.run_forever()
