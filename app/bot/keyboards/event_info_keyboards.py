from datetime import timedelta
from typing import List, Optional, Union
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.event_info import EventFilter, SelectEvent, SelectDate
from app.enums.discipline_types import DisciplineTypes
from app.enums.event_period import EventPeriod
from app.services.types.certain_event import CertainEvent
from app.services.types.general_event import GeneralEvent
from app.utils.get_discipline_type_name import (
    discipline_types,
    get_discipline_type_name,
)


def get_events_keyboard(events: List[GeneralEvent], tgid: int, filter_by: Optional[DisciplineTypes] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not filter_by:
        for event in events:
            builder.button(text=f"{get_discipline_type_name(event.discipline_type)} {event.name}", callback_data=SelectEvent(tg_id=tgid, event_id=event.id))
    else:
        for event in filter(lambda x: x.discipline_type.name == filter_by, events):
            builder.button(text=f"{get_discipline_type_name(event.discipline_type)} {event.name}", callback_data=SelectEvent(tg_id=tgid, event_id=event.id))

    builder.adjust(2, repeat=True)
    builder.row(InlineKeyboardButton(text="Cancel", callback_data=f"event_cancel:{tgid}"))
    return builder.as_markup()


def get_events_filter_keyboard(tgid: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for discipline_type in discipline_types:
        builder.button(text=f"{get_discipline_type_name(discipline_type)} {discipline_type.name}", callback_data=EventFilter(tg_id=tgid, type=discipline_type))

    builder.adjust(3, repeat=True)
    return builder.as_markup()


def get_events_dates(event: CertainEvent, week: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    carry = 0
    carry += 2 if event.period == EventPeriod.EVERY_FORTNIGHT else 1
    while carry <= 6:
        builder.button(text=f"{event.start_time.date()+timedelta(weeks=week)}", callback_data=SelectDate(week=week))
        week += carry
    builder.adjust(2, repeat=True)
    builder.row(InlineKeyboardButton(text="Інший час", callback_data=f"refresh:{week}"))
    return builder.as_markup()
