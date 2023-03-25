from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Chat
from pydantic import PositiveInt


async def get_user_by_id(bot: Bot, user_id: Optional[PositiveInt]) -> Optional[Chat]:
    if user_id is None:
        return None

    try:
        return await bot.get_chat(chat_id=user_id)
    except TelegramBadRequest:
        return None
