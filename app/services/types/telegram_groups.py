from typing import List

from pydantic import BaseModel, Field

from app.services.types.teleram_group import (
    TelegramGroup,
    TelegramGroupByTelegramIdResponse,
)


class TelegramGroups(BaseModel):
    groups: List[TelegramGroup]


class TelegramGroupsByTelegramId(BaseModel):
    telegram_groups: List[TelegramGroupByTelegramIdResponse] = Field(alias="telegramGroups")
