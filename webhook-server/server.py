import asyncio
from aiohttp import web
from mapper import register_webhook
from dispatcher import send_update

async def handler(request):
    if request.path == "/registerWebhook":
        data = await request.json()
        register_webhook(data["webhook_url"], data["username"])
    elif request.path == "/update":
        data = await request.json()
        await send_update(data)
    return web.Response(text="OK")


async def serve():
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    await site.start()

    print("======= Serving on http://127.0.0.1:8080/ ======")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(serve())
    loop.run_forever()
