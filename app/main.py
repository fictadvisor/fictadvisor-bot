import asyncio
import logging
import socket
from typing import List, Optional

import uvicorn

from app.api.factory import create_app
from app.bot.factory import create_bot, create_dispatcher
from app.settings import settings

bot = create_bot(token=settings.TOKEN.get_secret_value())
dispatcher = create_dispatcher()
app = create_app(
    bot=bot,
    dispatcher=dispatcher,
    webhook_secret=settings.TELEGRAM_SECRET.get_secret_value(),
)
logging.basicConfig(level="DEBUG")


class Server(uvicorn.Server):
    async def shutdown(self, sockets: Optional[List[socket.socket]] = None) -> None:
        await dispatcher.stop_polling()
        return await super().shutdown(sockets)


async def start() -> None:
    server = Server(uvicorn.Config(app, workers=1, loop="auto"))
    await asyncio.wait([
        asyncio.create_task(dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())),
        asyncio.create_task(server.serve())
    ])


def development() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
