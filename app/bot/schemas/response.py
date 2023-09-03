from uuid import UUID

from app.bot.schemas.base import BaseData
from app.enums.state import State


class ResponseData(BaseData, prefix="response"):
    method: State
    user_id: UUID
