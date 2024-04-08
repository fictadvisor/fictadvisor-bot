from datetime import timedelta
from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.event_info import EventFilter, SelectDate, SelectEvent
from app.enums.discipline_types import DisciplineTypes
from app.enums.event_period import EventPeriod
from app.services.types.certain_event import CertainEvent
from app.services.types.general_event import GeneralEvent
from app.utils.date_service import DateService
from app.utils.discipline_type import (
    discipline_types,
    get_discipline_type_color,
    get_discipline_type_ua_name,
)


def get_events_keyboard(events: List[GeneralEvent], filter_by: Optional[DisciplineTypes] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not filter_by:
        for event in events:
            builder.button(
                text=f"{get_discipline_type_color(event.discipline_type)} {event.name}", # type: ignore[arg-type]
                callback_data=SelectEvent(event_id=event.id)
            )
    else:
        for event in list(filter(lambda x: x.discipline_type.name == filter_by, events)): # type: ignore[arg-type, union-attr, assignment]
            builder.button(
                text=f"{get_discipline_type_color(event.discipline_type)} {event.name}", # type: ignore[arg-type]
                callback_data=SelectEvent(event_id=event.id)
            )

    builder.adjust(2, repeat=True)
    builder.row(
        InlineKeyboardButton(
            text="Cancel", callback_data="event_cancel"
        )
    )
    return builder.as_markup()


def get_events_filter_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for discipline_type in discipline_types:
        builder.button(
            text=f"{get_discipline_type_color(discipline_type)} {get_discipline_type_ua_name(discipline_type)}",
            callback_data=EventFilter(type=discipline_type)
        )

    builder.adjust(2, repeat=True)
    builder.button(
        text="🔄 До всього переліку",
        callback_data=EventFilter()
    )
    return builder.as_markup()


def get_events_dates(event: CertainEvent, week: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    step = 2 if event.period == EventPeriod.EVERY_FORTNIGHT else 1
    carry = 0
    if event.start_time < DateService.get_now():
        week += step
        carry += step
    for i in range(carry, DateService.get_least_of_weeks(), step):
        strdate = f"{(event.start_time.date()+timedelta(weeks=i)).strftime('%d.%m.%Y')}"
        builder.button(text=strdate, callback_data=SelectDate(
            week=week, strdate=strdate))
        week += step
    builder.adjust(2, repeat=True)
    builder.row(InlineKeyboardButton(
        text="Cancel", callback_data="date_cancel"))
    return builder.as_markup()


def get_approve() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Так", callback_data="APPROVE"),
        InlineKeyboardButton(text="Нє, змінити", callback_data="EDIT")
    )

    return builder.as_markup()
