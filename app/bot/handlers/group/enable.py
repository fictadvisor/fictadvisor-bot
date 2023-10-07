import logging

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.teleram_group import UpdateTelegramGroup


async def enable(message: Message) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
            already_enabled = any(telegram_group.post_info for telegram_group in telegram_groups.telegram_groups)
            for telegram_group in telegram_groups.telegram_groups:
                if not already_enabled:
                    await telegram_group_api.update(
                        telegram_group.group.id,
                        message.chat.id,
                        UpdateTelegramGroup(
                            post_info=True
                        )
                    )
                else:
                    await telegram_group_api.update(
                        telegram_group.group.id,
                        message.chat.id,
                        UpdateTelegramGroup(
                            post_info=False
                        )
                    )
            await message.answer("Сповіщення увімкнено" if not already_enabled else "Сповіщення вимкнено")
    except ResponseException as e:
        logging.error(e)
