from typing import Optional
from uuid import UUID

from pydantic import PositiveInt

from app.bot.schemas.base import BaseData
from app.enums.state import State


class CaptainData(BaseData, prefix="captain"):
    method: State
    user_id: UUID
    telegram_id: Optional[PositiveInt]
