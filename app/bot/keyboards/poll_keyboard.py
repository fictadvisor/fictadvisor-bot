from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.poll_answer import BackPoll, CancelPoll, PollAnswer
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.enums.poll import QuestionType
from app.services.types.users_teachers import UsersTeachers


def get_users_teachers_keyboard(users_teachers: UsersTeachers) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for teacher in users_teachers.teachers:
        builder.button(
            text=f"{teacher.last_name} {teacher.first_name[0]}.{teacher.middle_name[0]}.",
            callback_data=SelectTeacher(
                discipline_teacher_id=teacher.discipline_teacher_id)
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def get_poll_keyboard(
        question_id: str,
        question_step: int = 0,
        category_step: int = 0,
        question_type: QuestionType = QuestionType.SCALE
)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    sizes = []
    if question_type == QuestionType.SCALE:
        for i in range(1, 11):
            builder.button(text=f"{i}", callback_data=PollAnswer(
                question_id=question_id, value=str(i)))
        sizes.extend([5, 5])
    if question_step > 0 or category_step > 0:
        builder.button(text="back", callback_data=BackPoll()),
        builder.button(text="cancel", callback_data=CancelPoll())
        sizes.extend([2])
    else:
        builder.button(
            text="cancel", callback_data=CancelPoll()
            )
        sizes.extend([1])

    builder.adjust(*sizes)
    return builder.as_markup()
