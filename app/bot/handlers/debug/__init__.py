from aiogram import Router
from aiogram.filters import Command

from app.bot.handlers.debug.info import info

router = Router(name=__name__)

router.message.register(info, Command("debug"))
