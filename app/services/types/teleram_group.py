from pydantic import BaseModel, Field

from app.enums.telegram_source import TelegramSource


class UpdateTelegramGroup(BaseModel):
    source: TelegramSource


class CreateTelegramGroup(UpdateTelegramGroup):
    telegram_id: int = Field(alias="telegramId")


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")
