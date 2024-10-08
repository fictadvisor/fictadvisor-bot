from typing import List, Optional, Union
from uuid import UUID

from pydantic import Field

from app.enums.role import TeacherRole
from app.services.types.base import Base
from app.services.types.cathedra import Cathedra
from app.services.types.general_event import Subject


class Teacher(Base):
    id: Union[UUID, str]
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    middle_name: Optional[str] = Field(alias="middleName")
    description: Optional[str] = None
    avatar: str
    rating: float

class ExtendedTeacher(Teacher):
    roles: List[TeacherRole]
    cathedras: List[Cathedra]
    subject: Subject
    discipline_teacher_id: str = Field(alias="disciplineTeacherId")
