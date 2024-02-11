from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart

from app.bot.handlers.private.add_event_info import (
    add_homework_command,
    filter_event,
    select_event,
    cancel_select_event,
    select_date, 
    refresh_dates
)
from app.bot.handlers.private.fortnight import fortnight, select_week
from app.bot.handlers.private.left import left_command
from app.bot.handlers.private.next import next_command
from app.bot.handlers.private.now import now_command
from app.bot.handlers.private.start import start
from app.bot.handlers.private.today import today
from app.bot.handlers.private.today_events_infos import today_events_infos_command
from app.bot.handlers.private.tomorrow import tomorrow
from app.bot.handlers.private.tomorrow_events_infos import tomorrow_events_infos_command
from app.bot.handlers.private.week import week
from app.bot.keyboards.types.event_info import EventFilter, SelectEvent, SelectDate
from app.bot.keyboards.types.select_week import SelectWeek

router = Router(name=__name__)
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

router.message.register(start, CommandStart())
router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
router.message.register(fortnight, Command("fortnight"))
router.message.register(next_command, Command('next'))
router.message.register(now_command, Command("now"))
router.message.register(left_command, Command("left"))
router.message.register(add_homework_command, Command("add_homework"))
router.message.register(today_events_infos_command, Command("today_homework"))
router.message.register(tomorrow_events_infos_command, Command("tomorrow_homework"))
router.callback_query.register(cancel_select_event, F.data.startswith("event_cancel"))
router.callback_query.register(select_week, SelectWeek.filter())
router.callback_query.register(select_event, SelectEvent.filter())
router.callback_query.register(filter_event, EventFilter.filter())
router.callback_query.register(select_date, SelectDate.filter())
router.callback_query.register(refresh_dates, F.data.startswith("refresh"))
