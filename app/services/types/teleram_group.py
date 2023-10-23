from typing import Optional

from pydantic import Field

from app.enums.telegram_source import TelegramSource
from app.services.types.base import Base
from app.services.types.group import Group


class UpdateTelegramGroup(Base):
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    thread_id: Optional[int] = Field(None, alias="threadId")
    source: Optional[TelegramSource] = Field(None)
    post_info: Optional[bool] = Field(None, alias="postInfo")


class TelegramGroupData(Base):
    thread_id: Optional[int] = Field(None, alias="threadId")
    source: TelegramSource
    post_info: bool = Field(False, alias="postInfo")


class CreateTelegramGroup(TelegramGroupData):
    telegram_id: int = Field(alias="telegramId")


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")


class TelegramGroupByTelegramIdResponse(TelegramGroupData):
    group: Group
