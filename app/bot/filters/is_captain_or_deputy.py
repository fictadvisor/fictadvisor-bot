import logging
from typing import Dict, Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.enums.role import Role
from app.messages.eggs import get_random_punish
from app.services.exceptions.response_exception import ResponseException
from app.services.types.student import Student
from app.services.user_api import UserAPI
from app.utils.telegram import send_answer


class IsCaptainOrDeputy(Filter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> Union[bool, Dict[str, Student]]:
        try:
            async with UserAPI() as user_api:
                user = await user_api.get_user_by_telegram_id(update.from_user.id)  # type: ignore[union-attr]
            if user.group.role in (Role.CAPTAIN, Role.MODERATOR):
                return {"user": user}
        except ResponseException as e:
            await send_answer(update, "Прив'яжіть телеграм до аккаунта FictAdvisor")
            logging.error(e)
        else:
            if isinstance(update, CallbackQuery):
                await send_answer(update, get_random_punish(), show_alert=True)
            else:
                await send_answer(update, "Ця команда лише для старости або заступників")
        return False
