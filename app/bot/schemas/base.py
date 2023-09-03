from typing import Any

from aiogram.filters.callback_data import CallbackData
from pydantic import field_validator


class BaseData(CallbackData, prefix="base"):
    @field_validator('*', mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any) -> Any:
        if v == '':
            return None
        return v
