import re
from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.schemas.student import StudentData
from app.enums.states import States
from app.services.user_api import UserAPI


async def approve_student(callback: CallbackQuery, callback_data: StudentData) -> None:
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🟢 Заявка на студента {callback_data.user_id} схвалена.</b>",
        callback.message.html_text  # type: ignore[union-attr]
    )
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(  # type: ignore[union-attr]
        text=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Скасувати та видалити",
                                                                                 callback_data=StudentData(
                                                                                     method=States.DECLINED,
                                                                                     user_id=callback_data.user_id,
                                                                                     telegram_id=callback_data.telegram_id)
                                                                                 .pack())]])
    )


async def deny_student(callback: CallbackQuery, callback_data: StudentData) -> None:
    async with UserAPI() as api:
        await api.verify_student(
            student_id=callback_data.user_id,
            state=callback_data.method,
            is_captain=False
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🔴 Заявка на студента {callback_data.user_id} відхилена.</b>",
        callback.message.html_text  # type: ignore[union-attr]
    )
    if 'схвалена' in callback.message.text:  # type: ignore
        message = re.sub(
            r"<b>Ким</b>:.*",
            f"<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}",
            message,
            flags=re.S | re.M
        )
    else:

        message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(message)  # type: ignore[union-attr]
