from app.enums.telegram_source import TelegramSource
from app.services.types.update_telegram_group import UpdateTelegramGroup


class CreateTelegramGroup(UpdateTelegramGroup):
    source: TelegramSource
