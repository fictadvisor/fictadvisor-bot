from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart

from app.bot.handlers.private.add_event_info import (
    add_event_info,
    add_info_command,
    cancel,
    event_info_text_input,
    filter_event,
    refresh_dates,
    select_date,
    select_event,
)
from app.bot.handlers.private.fortnight import fortnight, select_week
from app.bot.handlers.private.left import left_command
from app.bot.handlers.private.next import next_command
from app.bot.handlers.private.next_week import next_week
from app.bot.handlers.private.now import now_command
from app.bot.handlers.private.start import start
from app.bot.handlers.private.today import today
from app.bot.handlers.private.tomorrow import tomorrow
from app.bot.handlers.private.week import week
from app.bot.keyboards.types.event_info import EventFilter, SelectDate, SelectEvent
from app.bot.keyboards.types.select_week import SelectWeek
from app.bot.states.event_info_states import AddEventInfoStates

router = Router(name=__name__)
router.message.filter(F.chat.type == ChatType.PRIVATE)
router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

router.message.register(start, CommandStart())
router.message.register(today, Command("today"))
router.message.register(tomorrow, Command("tomorrow"))
router.message.register(week, Command("week"))
router.message.register(next_week, Command("next_week"))
router.message.register(fortnight, Command("fortnight"))
router.message.register(next_command, Command('next'))
router.message.register(now_command, Command("now"))
router.message.register(left_command, Command("left"))
router.message.register(add_info_command, Command("add_info"))
router.message.register(event_info_text_input, AddEventInfoStates.text)
router.callback_query.register(add_event_info, F.data == "APPROVE")
router.callback_query.register(add_event_info, F.data == "EDIT")
router.callback_query.register(cancel, F.data.contains("cancel"))
router.callback_query.register(select_week, SelectWeek.filter())
router.callback_query.register(select_event, SelectEvent.filter())
router.callback_query.register(filter_event, EventFilter.filter())
router.callback_query.register(select_date, SelectDate.filter())
router.callback_query.register(refresh_dates, F.data.startswith("refresh"))
