import json
from aiohttp import web


class NetworkInterface:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    async def handler(self, request):
        if request.path == "/registerUpdater":
            updater_id = self.server.register_updater(request.url)
            users = self.server.balancer.allocate_user(updater_id)
            data = {
                "updater_id": updater_id,
                "users": [user.to_dict() for user in users],
            }
            return web.Response(
                text=json.dumps(data),
                content_type="application/json",
            )

    async def serve(self):
        server = web.Server(self.handler)
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.port)
        await site.start()

        print(f"======= Serving on http://127.0.0.1:{self.port}/ ======")
