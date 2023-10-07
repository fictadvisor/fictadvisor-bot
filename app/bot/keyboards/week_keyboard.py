from typing import Union
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.select_week import SelectWeek


def get_week_keyboard(week: int, group_id: Union[UUID, str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in range(1, 3):
        if i == week:
            builder.button(text=f"[ {i} ]", callback_data="ignore")
        else:
            builder.button(text=f"{i}", callback_data=SelectWeek(week=i, group_id=group_id))

    return builder.as_markup()
