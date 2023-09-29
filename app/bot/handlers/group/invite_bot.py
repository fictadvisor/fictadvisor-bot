from asyncio import sleep
from math import inf
from typing import MutableMapping, Union

from aiogram import Bot
from aiogram.types import (
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from cachetools import TTLCache

from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.teleram_group import UpdateTelegramGroup

cache: MutableMapping[int, bool] = TTLCache(maxsize=inf, ttl=10.0)


async def invite_bot(event: Union[ChatMemberUpdated, Message], bot: Bot) -> None:
    await sleep(1)
    if event.chat.id not in cache:
        await bot.send_message(
            chat_id=event.chat.id,
            text="Староста групи має натиснути цю кнопку",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Тиць", callback_data="captain_press")]]),
        )


async def migrate_chat(message: Message, migrate_from_chat_id: int) -> None:
    cache[message.chat.id] = True
    async with TelegramGroupAPI() as telegram_group_api:
        group = await telegram_group_api.get_by_telegram_id(migrate_from_chat_id)
        for telegram_group in group.telegram_groups:
            await telegram_group_api.update(
                telegram_group.group.id,
                migrate_from_chat_id,
                UpdateTelegramGroup(telegram_id=message.chat.id)
            )
