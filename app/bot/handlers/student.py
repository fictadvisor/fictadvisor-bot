from datetime import datetime
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from app.bot.schemas.student import StudentData
from app.services.user_api import State, UserAPI

student_router = Router(name=__name__)


@student_router.callback_query(StudentData.filter(
    F.method == State.APPROVED
))
async def approve_student(callback: CallbackQuery, callback_data: StudentData):
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = re.sub(r"^(.*)", f"<b>🟢 Заявка на студента {callback_data.user_id} схвалена.</b>", callback.message.html_text)
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Скасувати та видалити",
                                                                                 callback_data=StudentData(
                                                                                     method=State.DECLINED,
                                                                                     user_id=callback_data.user_id,
                                                                                     telegram_id=callback_data.telegram_id)
                                                                                 .pack())]])
    )


@student_router.callback_query(StudentData.filter(
    F.method == State.DECLINED
))
async def deny_student(callback: CallbackQuery, callback_data: StudentData):
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = re.sub(r"^(.*)", f"<b>🔴 Заявка на студента {callback_data.user_id} відхилена.</b>", callback.message.html_text)
    if 'схвалена' in callback.message.text:
        message = re.sub(r"<b>Ким</b>:.*", f"<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}", message, flags=re.S | re.M)
    else:
        message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(message)
