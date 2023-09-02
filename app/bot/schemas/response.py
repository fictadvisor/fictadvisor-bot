from uuid import UUID

from aiogram.filters.callback_data import CallbackData

from app.enums.states import States


class ResponseData(CallbackData, prefix="response"):
    method: States
    user_id: UUID
