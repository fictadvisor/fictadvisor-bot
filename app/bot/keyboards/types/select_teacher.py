
from aiogram.filters.callback_data import CallbackData


class SelectTeacher(CallbackData, prefix="teacher"):
    discipline_teacher_id: str
