from typing import Optional

from pydantic import Field

from app.enums.telegram_source import TelegramSource
from app.services.types.base import Base
from app.services.types.group import Group


class UpdateTelegramGroup(Base):
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    thread_id: Optional[int] = Field(None, alias="threadId")
    source: Optional[TelegramSource] = Field(None)


class CreateTelegramGroup(Base):
    telegram_id: int = Field(alias="telegramId")
    thread_id: Optional[int] = Field(None, alias="threadId")
    source: TelegramSource


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")


class TelegramGroupByTelegramIdResponse(UpdateTelegramGroup):
    group: Group
