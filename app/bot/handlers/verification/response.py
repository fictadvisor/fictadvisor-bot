import re
from datetime import datetime
from uuid import UUID

from aiogram.types import CallbackQuery

from app.bot.schemas.response import ResponseData
from app.services.response_api import ResponseAPI


async def approve_response(callback: CallbackQuery, callback_data: ResponseData) -> None:
    entities = [el.extract_from(callback.message.text) for el in   # type: ignore[union-attr]
                filter(lambda x: x.type == "code", callback.message.entities)]   # type: ignore

    async with ResponseAPI() as api:
        await api.verify_response(
            discipline_teacher_id=UUID(entities[1]),
            question_id=UUID(entities[0]),
            user_id=callback_data.user_id,
            value=entities[2]
        )

    message = re.sub(r"^(.*)", f"<b>🟢 Відгук {entities[1]} схвалено.</b>",
                     callback.message.html_text)  # type: ignore[union-attr]
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(text=message)  # type: ignore[union-attr]


async def deny_response(callback: CallbackQuery) -> None:
    entities = [el.extract_from(callback.message.text) for el in  # type: ignore[union-attr]
                filter(lambda x: x.type == "code", callback.message.entities)]  # type: ignore
    message = re.sub(r"^(.*)", f"<b>🔴 Відгук {entities[1]} відхилено.</b>",
                     callback.message.html_text)  # type: ignore[union-attr]
    if 'схвалена' in callback.message.text:  # type: ignore
        message = re.sub(r"<b>Ким</b>:.*",
                         f"<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}", message,
                         flags=re.S | re.M)
    else:
        message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(message)  # type: ignore[union-attr]
