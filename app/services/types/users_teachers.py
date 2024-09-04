from typing import List

from pydantic import Field

from app.services.types.base import Base
from app.services.types.teacher import ExtendedTeacher


class UsersTeachers(Base):
    selected_in_last_semester: bool = Field(alias="hasSelectedInLastSemester")
    teachers: List[ExtendedTeacher]

