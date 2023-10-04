import logging

from aiogram.types import CallbackQuery

from app.enums.role import Role
from app.enums.telegram_source import TelegramSource
from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.teleram_group import CreateTelegramGroup
from app.services.user_api import UserAPI


async def captain_button_press_callback(callback: CallbackQuery) -> None:
    async with (
        TelegramGroupAPI() as telegram_group_api,
        UserAPI() as user_api,
    ):
        try:
            user_id = callback.from_user.id
            user = await user_api.get_user_by_telegram_id(user_id)
            group = user.group

            if group.role not in (Role.CAPTAIN, Role.MODERATOR):
                await callback.answer("Ти не староста!")
                return

            await telegram_group_api.create(group.id,
                                            CreateTelegramGroup(
                                                source=TelegramSource.GROUP,
                                                telegram_id=callback.message.chat.id))  # type: ignore[union-attr]
            await callback.message.edit_text("Групу додано")  # type: ignore[union-attr]
        except ResponseException as e:
            await callback.answer(e.message)
            logging.error(e)
