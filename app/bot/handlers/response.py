import re
from datetime import datetime
from uuid import UUID

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.schemas.response import ResponseData
from app.services.response_api import ResponseAPI
from app.services.user_api import State

response_router = Router(name=__name__)


@response_router.callback_query(ResponseData.filter(
    F.method == State.APPROVED
))
async def approve_response(callback: CallbackQuery, callback_data: ResponseData):
    entities = [el.extract_from(callback.message.text) for el in
                filter(lambda x: x.type == "code", callback.message.entities)]

    async with ResponseAPI() as api:
        await api.verify_response(
            discipline_teacher_id=callback_data.discipline_teacher_id,
            question_id=UUID(entities[0]),
            user_id=UUID(entities[1]),
            value=entities[2]
        )

    message = re.sub(r"^(.*)", f"<b>🟢 Відгук {callback_data.discipline_teacher_id} схвалено.</b>",
                     callback.message.html_text)
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(text=message)


@response_router.callback_query(ResponseData.filter(
    F.method == State.DECLINED
))
async def deny_response(callback: CallbackQuery, callback_data: ResponseData):
    message = re.sub(r"^(.*)", f"<b>🔴 Відгук {callback_data.discipline_teacher_id} відхилено.</b>",
                     callback.message.html_text)
    if 'схвалена' in callback.message.text:
        message = re.sub(r"<b>Ким</b>:.*",
                         f"<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}", message,
                         flags=re.S | re.M)
    else:
        message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(message)
