from typing import Optional

from aiogram.types import Message

from app.enums.telegram_source import TelegramSource
from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.telegram_groups import (
    TelegramGroups,
)
from app.services.types.teleram_group import (
    CreateTelegramGroup,
    TelegramGroup,
    UpdateTelegramGroup,
)
from app.services.user_api import UserAPI


async def enable(message: Message) -> None:
    async with UserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    async with TelegramGroupAPI() as telegram_group_api:
        try:
            telegram_groups: TelegramGroups = await telegram_group_api.get_telegram_groups(user.group.id)
            telegram_group: Optional[TelegramGroup] = next(filter(lambda x: (x.source == TelegramSource.PERSONAL_CHAT and x.telegram_id == message.from_user.id), telegram_groups.telegram_groups), None) # type: ignore
            if not telegram_group:
                telegram_group = await telegram_group_api.create(
                    user.group.id,
                    CreateTelegramGroup(
                        source=TelegramSource.PERSONAL_CHAT,
                        post_info=True,
                        telegram_id=message.chat.id
                    )
                )
            else:
                telegram_group = await telegram_group_api.update(
                    user.group.id,
                    message.chat.id,
                    UpdateTelegramGroup(
                        post_info=not telegram_group.post_info
                    )
                )
        except ResponseException:
            telegram_group = await telegram_group_api.create(
                user.group.id,
                CreateTelegramGroup(
                    source=TelegramSource.PERSONAL_CHAT,
                    post_info=True,
                    telegram_id=message.chat.id
                )
            )
    await message.reply("Сповіщення увімкнено" if telegram_group.post_info else "Сповіщення вимкнено")
