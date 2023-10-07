from aiogram import Router
from aiogram.filters import Command

from app.bot.handlers.schedule.fortnight import fortnight, select_week
from app.bot.handlers.schedule.today import today
from app.bot.handlers.schedule.tomorrow import tomorrow
from app.bot.handlers.schedule.week import week
from app.bot.keyboards.types.select_week import SelectWeek

router = Router()

router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
router.message.register(fortnight, Command("fortnight"))
router.callback_query.register(select_week, SelectWeek.filter())
