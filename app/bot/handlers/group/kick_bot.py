import logging

from aiogram.types import ChatMemberUpdated

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI


async def kick_bot(event: ChatMemberUpdated) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        try:
            group = await telegram_group_api.get_by_telegram_id(event.chat.id)
            for telegram_group in group.telegram_groups:
                await telegram_group_api.delete(telegram_group.group.id, event.chat.id)
        except ResponseException as e:
            logging.error(e)
