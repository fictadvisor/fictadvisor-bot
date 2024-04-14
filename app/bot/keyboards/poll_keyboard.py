from typing import Union
from uuid import UUID

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.keyboards.types.select_teacher import SelectTeacher

from app.services.types.users_teachers import UsersTeachers


def get_poll_keyboard(users_teachers: UsersTeachers) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for teacher in users_teachers.teachers:
        builder.button(
            text=f"{teacher.last_name} {teacher.first_name[0]}.{teacher.middle_name[0]}.",
            callback_data=SelectTeacher(discipline_teacher_id=teacher.discipline_teacher_id)
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()
