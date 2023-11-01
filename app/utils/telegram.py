from typing import Optional, Union

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Chat, Message
from pydantic import PositiveInt


async def get_user_by_id(bot: Bot, user_id: Optional[PositiveInt]) -> Optional[Chat]:
    if user_id is None:
        return None

    try:
        return await bot.get_chat(chat_id=user_id)
    except TelegramBadRequest:
        return None


async def send_answer(update: Union[Message, CallbackQuery], message: str) -> None:
    if isinstance(update, Message):
        await update.reply(message)
    else:
        await update.answer(message)

