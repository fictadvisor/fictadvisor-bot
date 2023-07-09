from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.services.user_api import State


class ResponseData(CallbackData, prefix="response"):
    method: State
    user_id: UUID
