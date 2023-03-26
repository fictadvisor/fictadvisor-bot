from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from app.bot.handlers.debug import debug_router
from app.bot.handlers.student import student_router
from app.bot.handlers.superhero import superhero_router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    for router in [debug_router, student_router, superhero_router]:
        dispatcher.include_router(router)

    return dispatcher


def create_bot(token: str) -> Bot:
    return Bot(token=token, parse_mode=ParseMode.HTML)
