from datetime import timedelta
from typing import List, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.event_info import (
    EventApprove,
    EventCancel,
    EventEdit,
    EventFilter,
    SelectDate,
    SelectEvent,
)
from app.enums.cancel_types import CancelType
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
                text=f"{get_discipline_type_color(event.discipline_type)} {event.name}",
                callback_data=SelectEvent(event_id=event.id)
            )
    else:
        new_events = list(filter(lambda x: x.discipline_type.name == filter_by, events))  # type: ignore[arg-type, union-attr]
        for event in new_events:  # type: ignore[assignment]
            builder.button(
                text=f"{get_discipline_type_color(event.discipline_type)} {event.name}",
                callback_data=SelectEvent(event_id=event.id)
            )
    builder.button(
        text="Cancel", callback_data=EventCancel(cancel_type=CancelType.EVENT)
    )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def get_events_filter_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for discipline_type in discipline_types:
        builder.button(
            text=f"{get_discipline_type_color(discipline_type)} {get_discipline_type_ua_name(discipline_type)}",
            callback_data=EventFilter(type=discipline_type)
        )

    builder.button(
        text="🔄 До всього переліку",
        callback_data=EventFilter()
    )
    builder.adjust(2, repeat=True)
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
    builder.button(
        text="Cancel", callback_data=EventCancel(cancel_type=CancelType.DATE)
    )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def get_approve() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Так", callback_data=EventApprove())
    builder.button(text="Нє, змінити", callback_data=EventEdit())

    return builder.as_markup()
