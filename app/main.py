import asyncio
import logging
import socket
import sys
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


if settings.DEVELOPMENT:
    from pyngrok import ngrok
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    public_url = ngrok.connect(port).public_url
    settings.BASE_URL = public_url
    logging.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
