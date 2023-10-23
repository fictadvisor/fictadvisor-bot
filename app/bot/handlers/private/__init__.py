from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart

from app.bot.handlers.private.fortnight import fortnight, select_week
from app.bot.handlers.private.start import start
from app.bot.handlers.private.today import today
from app.bot.handlers.private.tomorrow import tomorrow
from app.bot.handlers.private.week import week
from app.bot.keyboards.types.select_week import SelectWeek

router = Router(name=__name__)
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

router.message.register(start, CommandStart())
router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
router.message.register(fortnight, Command("fortnight"))
router.callback_query.register(select_week, SelectWeek.filter())
