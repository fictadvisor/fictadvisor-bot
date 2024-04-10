from typing import Union
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class SelectTeacher(CallbackData, prefix="teacher"):
    teacher_id: Union[UUID, str]
