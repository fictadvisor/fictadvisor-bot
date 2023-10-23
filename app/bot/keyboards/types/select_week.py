from typing import Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SelectWeek(CallbackData, prefix="fortnight"):
    group_id: Union[UUID, str]
    week: int
