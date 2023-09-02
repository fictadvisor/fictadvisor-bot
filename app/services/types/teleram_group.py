from pydantic import Field

from app.services.types.update_telegram_group import UpdateTelegramGroup


class TelegramGroup(UpdateTelegramGroup):
    group_id: str = Field(alias="groupId")
