import re
from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.schemas.captain import CaptainData
from app.enums.state import State
from app.services.types.student import VerifyStudent
from app.services.user_api import UserAPI


async def approve_captain(callback: CallbackQuery, callback_data: CaptainData) -> None:
    async with UserAPI() as api:
        await api.verify_student(
            callback_data.user_id,
            VerifyStudent(
                state=callback_data.method,
                is_captain=True
            )
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🟢 Заявка на старосту {callback_data.user_id} схвалена.</b>",
        callback.message.html_text  # type: ignore[union-attr]
    )
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(  # type: ignore[union-attr]
        text=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Скасувати та видалити",
                                                                                 callback_data=CaptainData(
                                                                                     method=State.DECLINED,
                                                                                     user_id=callback_data.user_id,
                                                                                     telegram_id=callback_data.telegram_id)
                                                                                 .pack())]])
    )


async def deny_captain(callback: CallbackQuery, callback_data: CaptainData) -> None:
    async with UserAPI() as api:
        await api.verify_student(
            callback_data.user_id,
            VerifyStudent(
                state=callback_data.method,
                is_captain=True
            )
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🔴 Заявка на старосту {callback_data.user_id} відхилена.</b>",
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
