from pydantic import Field

from app.services.types.update_telegram_group import UpdateTelegramGroup


class CreateTelegramGroup(UpdateTelegramGroup):
    telegram_id: int = Field(alias="telegramId")
