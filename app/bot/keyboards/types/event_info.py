from typing import Optional, Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.enums.cancel_types import CancelType
from app.enums.discipline_types import DisciplineTypes


class SelectEvent(CallbackData, prefix="event_info"):
    event_id: Union[UUID, str]


class EventFilter(CallbackData, prefix="event_filter"):
    type: Optional[DisciplineTypes] = None


class SelectDate(CallbackData, prefix="event_date"):
    week: int
    strdate: str


class EventCancel(CallbackData, prefix="event_cancel"):
    cancel_type: CancelType


class EventEdit(CallbackData, prefix="event_edit"):
    pass


class EventApprove(CallbackData, prefix="event_approve"):
    pass
