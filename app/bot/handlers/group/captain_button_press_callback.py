import logging

from aiogram.types import CallbackQuery

from app.enums.role import Role
from app.enums.telegram_source import TelegramSource
from app.services.exceptions.response_exception import ResponseException
from app.services.telegram_group_api import TelegramGroupAPI
from app.services.types.student import Student
from app.services.types.teleram_group import CreateTelegramGroup


async def captain_button_press_callback(callback: CallbackQuery, user: Student) -> None:
    async with TelegramGroupAPI() as telegram_group_api:
        try:
            group = user.group

            if group.role not in (Role.CAPTAIN, Role.MODERATOR):
                await callback.answer("В тебе немає прав")
                return

            try:
                await telegram_group_api.get_by_telegram_id(callback.message.chat.id) # type: ignore[union-attr]
            except ResponseException:
                await telegram_group_api.create(group.id,
                                                CreateTelegramGroup(
                                                    source=TelegramSource.GROUP,
                                                    telegram_id=callback.message.chat.id))  # type: ignore[union-attr]
                await callback.message.edit_text("Чат прикріплено")  # type: ignore[union-attr]
            else:
                await callback.answer("В даному чаті вже прикріплена група.")

        except ResponseException as e:
            await callback.answer(e.message)
            logging.error(e)
