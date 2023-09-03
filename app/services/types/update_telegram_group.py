from pydantic import BaseModel

from app.enums.telegram_source import TelegramSource


class UpdateTelegramGroup(BaseModel):
    source: TelegramSource
