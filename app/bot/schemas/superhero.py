from typing import Optional
from uuid import UUID

from aiogram.filters.callback_data import CallbackData
from pydantic import PositiveInt

from app.services.user_api import State


class SuperheroData(CallbackData, prefix="hero"):
    method: State
    user_id: UUID
    telegram_id: Optional[PositiveInt]
