from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart

from app.bot.handlers.private.start import start

router = Router(name=__name__)
router.message.filter(F.chat.type == ChatType.PRIVATE)

router.message.register(start, CommandStart)
