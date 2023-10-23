import logging
from typing import Optional

from aiogram.types import Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.student import Student
from app.services.types.telegram_groups import TelegramGroupsByTelegramId
from app.services.types.teleram_group import TelegramGroup, UpdateTelegramGroup


async def enable(message: Message, user: Student, telegram_groups: TelegramGroupsByTelegramId) -> None:
    try:
        async with TelegramGroupAPI() as telegram_group_api:
            telegram_group: Optional[TelegramGroup] = next(filter(lambda x: x.group.id == user.group.id, telegram_groups.telegram_groups), None)  # type: ignore
            if not telegram_group:
                await message.reply("Цей чат не твоєї групи")
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
            await message.reply("Сповіщення увімкнено" if not telegram_group.post_info else "Сповіщення вимкнено")
    except ResponseException as e:
        logging.error(e)
