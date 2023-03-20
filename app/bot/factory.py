from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from app.bot.handlers.debug import debug_router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher.include_router(debug_router)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
