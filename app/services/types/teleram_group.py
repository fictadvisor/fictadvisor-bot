from pydantic import BaseModel, ConfigDict, Field

from app.enums.telegram_source import TelegramSource
from app.services.types.group import Group


class UpdateTelegramGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    source: TelegramSource


class CreateTelegramGroup(UpdateTelegramGroup):
    telegram_id: int = Field(alias="telegramId")


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")


class TelegramGroupByTelegramIdResponse(UpdateTelegramGroup):
    group: Group
