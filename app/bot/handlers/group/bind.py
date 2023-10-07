import logging

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.teleram_group import UpdateTelegramGroup


async def bind(message: Message) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_groups = await telegram_group_api.get_by_telegram_id(message.chat.id)
            for telegram_group in telegram_groups.telegram_groups:
                await telegram_group_api.update(
                    telegram_group.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        thread_id=message.reply_to_message.message_id  # type: ignore[union-attr]
                    )
                )
            await message.answer("Гілку прикріплено")
    except ResponseException as e:
        logging.error(e)
