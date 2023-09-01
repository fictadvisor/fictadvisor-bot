from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt


class BroadcastSuperhero(BaseModel):
    id: UUID
    telegram_id: Optional[PositiveInt] = Field(None, alias="telegramId")
    first_name: str = Field(..., alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: str = Field(..., alias="lastName")
    group_code: str = Field(..., alias="groupCode")
    dorm: bool
