from typing import Optional
from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from pydantic import PositiveInt

from app.enums.states import States


class StudentData(CallbackData, prefix="student"):
    method: States
    user_id: UUID
    telegram_id: Optional[PositiveInt]
