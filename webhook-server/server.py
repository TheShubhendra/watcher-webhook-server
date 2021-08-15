import asyncio
from aiohttp import web
from decouple import config


PORT = config("PORT", 5000)


async def handler(request):
    if request.path == "registerUpdater":
        return web.Response(
            json="""{
                "updater_id":5,
                "users":[
                    "username":"Shubhendra-Kushwaha-1",
                    "user_id":5
                    ]
                
            }"""
        )
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
    site = web.TCPSite(runner, "localhost", PORT)
    await site.start()

    print(r"======= Serving on http://127.0.0.1:{PORT}/ ======")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(serve())
    loop.run_forever()
