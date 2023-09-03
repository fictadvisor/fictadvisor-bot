from pydantic import Field

from app.services.types.create_telegram_group import CreateTelegramGroup


class TelegramGroup(CreateTelegramGroup):
    group_id: str = Field(alias="groupId")
