import asyncio
from .server import serve
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)

loop = asyncio.get_event_loop()
loop.create_task(serve())
loop.run_forever()
