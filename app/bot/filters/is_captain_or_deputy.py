import logging
from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.enums.role import Role
from app.services.exceptions.response_exception import ResponseException
from app.services.user_api import UserAPI


class IsCaptainOrDeputy(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        try:
            async with UserAPI() as user_api:
                user = await user_api.get_user_by_telegram_id(update.from_user.id)  # type: ignore[union-attr]
            if user.group.role in (Role.CAPTAIN, Role.MODERATOR):
                return True
        except ResponseException as e:
            logging.error(e)
        return False
