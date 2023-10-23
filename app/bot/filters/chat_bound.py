import logging
from typing import Dict, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.telegram_groups import TelegramGroupsByTelegramId


class ChatBound(Filter):
    @staticmethod
    def get_chat_id(update: Union[Message, CallbackQuery]) -> int:
        if isinstance(update, CallbackQuery):
            return update.message.chat.id  # type: ignore[union-attr]
        return update.chat.id

    async def __call__(self, update: Union[Message, CallbackQuery]) -> Union[Dict[str, TelegramGroupsByTelegramId], bool]:
        try:
            async with TelegramGroupAPI() as telegram_group_api:
                telegram_groups = await telegram_group_api.get_by_telegram_id(self.get_chat_id(update))  # type: ignore[union-attr]
            return {"telegram_groups": telegram_groups}
        except ResponseException as e:
            if isinstance(update, Message):
                await update.answer("Чат не закріплено за жодною групою, пропишіть /start")
            logging.error(e)
        return False
