from pydantic import Field

from app.enums.telegram_source import TelegramSource
from app.services.types.base import Base
from app.services.types.group import Group


class UpdateTelegramGroup(Base):
    source: TelegramSource


class CreateTelegramGroup(UpdateTelegramGroup):
    telegram_id: int = Field(alias="telegramId")


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")


class TelegramGroupByTelegramIdResponse(UpdateTelegramGroup):
    group: Group
