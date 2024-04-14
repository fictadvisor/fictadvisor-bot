from typing import List
from app.services.types.teacher import ExtendedTeacher
from pydantic import Field

from app.services.types.base import Base


class UsersTeachers(Base):
    selected_in_last_semester: bool = Field(alias="hasSelectedInLastSemester")
    teachers: List[ExtendedTeacher]

