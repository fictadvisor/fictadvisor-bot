import logging
from typing import Optional

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.student import Student
from app.services.types.teleram_group import TelegramGroup, UpdateTelegramGroup


async def enable(message: Message, user: Student) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_groups = await telegram_group_api.get_telegram_groups(user.group.id)
            telegram_group: Optional[TelegramGroup] = next(filter(lambda x: x.telegram_id == message.chat.id, telegram_groups.telegram_groups), None)  # type: ignore
            if not telegram_group:
                return
            if not telegram_group.post_info:
                await telegram_group_api.update(
                    user.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        post_info=True
                    )
                )
            else:
                await telegram_group_api.update(
                    user.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        post_info=False
                    )
                )
            await message.answer("Сповіщення увімкнено" if not telegram_group.post_info else "Сповіщення вимкнено")
    except ResponseException as e:
        logging.error(e)
