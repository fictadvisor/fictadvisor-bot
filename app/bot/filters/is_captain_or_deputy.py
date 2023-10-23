import logging
from typing import Dict, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.enums.role import Role
from app.services.exceptions.response_exception import ResponseException
from app.services.types.student import Student
from app.services.user_api import UserAPI


class IsCaptainOrDeputy(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> Union[bool, Dict[str, Student]]:
        try:
            async with UserAPI() as user_api:
                user = await user_api.get_user_by_telegram_id(update.from_user.id)  # type: ignore[union-attr]
            if user.group.role in (Role.CAPTAIN, Role.MODERATOR):
                return {"user": user}
        except ResponseException as e:
            if isinstance(update, Message):
                await update.reply("Прив'яжіть телеграм до аккаунта FictAdvisor")
            logging.error(e)
        else:
            if isinstance(update, Message):
                await update.reply("Ця команда лише для старости або заступників")
        return False
