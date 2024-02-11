from typing import Optional, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.enums.discipline_types import DisciplineTypes


class SelectEvent(CallbackData, prefix="eventInfo"):
    event_id: Union[UUID, str]


class EventFilter(CallbackData, prefix="eventFilter"):
    type: DisciplineTypes


class SelectDate(CallbackData, prefix="date"):
    week: int
