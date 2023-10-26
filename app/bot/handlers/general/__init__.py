from aiogram import Router
from aiogram.filters import Command

from app.bot.handlers.general.help import help_command

router = Router(name=__name__)

router.message.register(help_command, Command("help"))
