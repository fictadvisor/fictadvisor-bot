from typing import List

from pydantic import Field

from app.services.types.base import Base
from app.services.types.teleram_group import (
    TelegramGroup,
    TelegramGroupByTelegramIdResponse,
)


class TelegramGroups(Base):
    groups: List[TelegramGroup]


class TelegramGroupsByTelegramId(Base):
    telegram_groups: List[TelegramGroupByTelegramIdResponse] = Field(alias="telegramGroups")
