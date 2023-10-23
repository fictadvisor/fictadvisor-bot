import logging
from typing import Optional

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.student import Student
from app.services.types.teleram_group import TelegramGroup, UpdateTelegramGroup


async def bind(message: Message, user: Student) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_groups = await telegram_group_api.get_telegram_groups(user.group.id)
            telegram_group: Optional[TelegramGroup] = next(filter(lambda x: x.telegram_id == message.chat.id, telegram_groups.telegram_groups), None)  # type: ignore
            if not telegram_group:
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
            await message.answer("Гілку прикріплено" if telegram_group.thread_id != message.reply_to_message.message_id else "Гілку відкріплено")  # type: ignore[union-attr]
    except ResponseException as e:
        logging.error(e)
