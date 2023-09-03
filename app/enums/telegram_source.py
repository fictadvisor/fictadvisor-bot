from enum import Enum


class TelegramSource(str, Enum):
    GROUP = 'GROUP'
    CHANNEL = 'CHANNEL'
    PERSONAL_CHAT = 'PERSONAL_CHAT'
