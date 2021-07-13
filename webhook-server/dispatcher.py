import api_database as db
import aiohttp


async def send_update(update):
    webhook_urls = db.get_webhook_urls(update["username"])
    async with aiohttp.ClientSession() as session:
        for url in webhook_urls:
            await session.post(webhook_urls, json=update)
