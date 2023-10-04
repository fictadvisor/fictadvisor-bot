from aiogram import Router
from aiogram.filters import Command

from app.bot.handlers.schedule.today import today
from app.bot.handlers.schedule.tomorrow import tomorrow
from app.bot.handlers.schedule.week import week

router = Router()

router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
