from typing import Union
from uuid import UUID

from pydantic import Field

from app.services.types.base import Base


class RegisterTelegram(Base):
    token: Union[UUID, str]
    telegram_id: int = Field(alias="telegramId")
