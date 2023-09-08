from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field


class RegisterTelegram(BaseModel):
    token: Union[UUID, str]
    telegram_id: int = Field(serialization_alias="telegramId")
