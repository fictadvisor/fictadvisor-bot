import re
from datetime import datetime

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.schemas.superhero import SuperheroData
from app.services.user_api import State, UserAPI


async def approve_superhero(callback: CallbackQuery, callback_data: SuperheroData) -> None:
    async with UserAPI() as api:
        await api.verify_superhero(
            student_id=callback_data.user_id,
            state=callback_data.method
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🟢 Заявка на супергероя {callback_data.user_id} схвалена.</b>",
        callback.message.html_text  # type: ignore[union-attr]
    )
    message += f"\n\n<b>Ким</b>: {callback.from_user.mention_html()}\n<b>Коли:</b> {datetime.now()}"
    await callback.message.edit_text(  # type: ignore[union-attr]
        text=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Скасувати та видалити",
                                                                                 callback_data=SuperheroData(
                                                                                     method=State.DECLINED,
                                                                                     user_id=callback_data.user_id,
                                                                                     telegram_id=callback_data.telegram_id)
                                                                                 .pack())]])
    )


async def deny_superhero(callback: CallbackQuery, callback_data: SuperheroData) -> None:
    async with UserAPI() as api:
        await api.verify_superhero(
            student_id=callback_data.user_id,
            state=callback_data.method
        )

    message = re.sub(
        r"^(.*)",
        f"<b>🔴 Заявка на супергероя {callback_data.user_id} відхилена.</b>",
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
