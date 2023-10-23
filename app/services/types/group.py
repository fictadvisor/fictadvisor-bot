from typing import List, Optional, Union
from uuid import UUID

from pydantic import Field

from app.enums.role import Role
from app.enums.state import State
from app.enums.telegram_source import TelegramSource
from app.services.types.base import Base


class Group(Base):
    id: Union[UUID, str]
    code: str


class TelegramGroup(Base):
    telegram_id: int = Field(alias="telegramId")
    thread_id: Optional[int] = Field(alias="threadId")
    source: TelegramSource
    post_info: bool = Field(False, alias="postInfo")


class ExtendedGroup(Group):
    state: State
    role: Role


class GroupWithTelegramGroupsResponse(Base):
    id: Union[UUID, str]
    telegram_groups: List[TelegramGroup] = Field(alias="telegramGroups")
