
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.types.poll_answer import (
    BackPoll,
    CancelPoll,
    PollAnswer,
    SubmitPoll,
)
from app.bot.keyboards.types.select_teacher import SelectTeacher
from app.enums.poll import QuestionType
from app.services.types.question import Question
from app.services.types.users_teachers import UsersTeachers
from app.utils.emoji import Emoji


def get_users_teachers_keyboard(users_teachers: UsersTeachers) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for teacher in users_teachers.teachers:
        builder.button(
            text=f"{teacher.last_name} {teacher.first_name[0]}.{teacher.middle_name[0]}." if teacher.middle_name else f"{teacher.last_name} {teacher.first_name[0]}.",
            callback_data=SelectTeacher(discipline_teacher_id=teacher.discipline_teacher_id)
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def get_poll_keyboard(
        question: Question,
        question_step: int = 0,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    sizes = []
    if question.type == QuestionType.SCALE:
        for i in range(1, 11):
            builder.button(
                text=f"{Emoji.from_number(i)}",
                callback_data=PollAnswer(
                    question_id=question.id,
                    value=f"{i}")
            )
        sizes.extend([5, 5])
    if question.type == QuestionType.TOGGLE:
        builder.button(
            text="Так",
            callback_data=PollAnswer(
                question_id=question.id,
                value="1"
            )
        )
        builder.button(
            text="Ні",
            callback_data=PollAnswer(
                question_id=question.id,
                value="0"
            )
        )

    if question_step > 0:
        if question.type == QuestionType.TEXT:
            builder.button(
                text=f"{Emoji.SKIP} Пропустити",
                callback_data=PollAnswer(
                    question_id=question.id,
                    value="----"
                )
            )
            sizes.extend([1])
        builder.button(
            text=f"{Emoji.BACK} Назад",
            callback_data=BackPoll()),
        builder.button(
            text=f"{Emoji.CANCEL} Скасувати",
            callback_data=CancelPoll())
    else:
        builder.button(
            text=f"{Emoji.CANCEL} Скасувати",
            callback_data=CancelPoll()
        )
    sizes.extend([2])

    builder.adjust(*sizes)
    return builder.as_markup()


def get_submit_edit_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"{Emoji.BACK} Повернутись до опитування",
        callback_data=BackPoll()
    ),
    builder.button(
        text=f"{Emoji.SAVE} Надіслати відповіді",
        callback_data=SubmitPoll()
    )
    return builder.as_markup()
