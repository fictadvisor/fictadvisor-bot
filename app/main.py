import asyncio
import logging

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


async def start() -> None:
    server = uvicorn.Server(uvicorn.Config(app, workers=1, loop="asyncio"))
    await asyncio.wait([
        asyncio.create_task(dispatcher.start_polling(bot, allowed_updates=dispatcher.resolve_used_update_types())),
        asyncio.create_task(server.serve())
    ])


def development() -> None:
    asyncio.run(start())
