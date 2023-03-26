from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.schemas.student import StudentData
from app.services.user_api import State, UserAPI

student_router = Router(name=__name__)


@student_router.callback_query(StudentData.filter(
    F.method == State.APPROVED
))
async def echo_handler(callback: CallbackQuery, callback_data: StudentData):
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = callback.message.html_text.replace("<b>Заявка на студента</b>",
                                                 f"<b>🟢 Заявка на студента {callback_data.user_id} схвалена.</b>")
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
async def echo_handler(callback: CallbackQuery, callback_data: StudentData):
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = callback.message.html_text.replace("<b>Заявка на студента</b>",
                                                 f"<b>🔴 Заявка на студента {callback_data.user_id} відхилена.</b>")
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(message)
