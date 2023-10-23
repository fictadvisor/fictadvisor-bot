import logging
from typing import Optional

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.student import Student
from app.services.types.telegram_groups import TelegramGroupsByTelegramId
from app.services.types.teleram_group import TelegramGroup, UpdateTelegramGroup


async def bind(message: Message, user: Student, telegram_groups: TelegramGroupsByTelegramId) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_group: Optional[TelegramGroup] = next(filter(lambda x: x.group.id == user.group.id, telegram_groups.telegram_groups), None)  # type: ignore
            if not telegram_group:
                await message.reply("Цей чат не твоєї групи")
                return
            if telegram_group.thread_id != message.reply_to_message.message_id:  # type: ignore[union-attr]
                await telegram_group_api.update(
                    user.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        thread_id=message.reply_to_message.message_id  # type: ignore[union-attr]
                    )
                )
            else:
                await telegram_group_api.update(
                    user.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        thread_id=None
                    )
                )
            await message.reply("Гілку прикріплено" if telegram_group.thread_id != message.reply_to_message.message_id else "Гілку відкріплено")  # type: ignore[union-attr]
    except ResponseException as e:
        logging.error(e)
