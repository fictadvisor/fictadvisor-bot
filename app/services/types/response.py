from typing import Union, List
from uuid import UUID

from pydantic import Field

from app.services.types.base import Base
from app.services.types.teacher import Teacher
from app.services.types.general_event import Subject
from app.services.types.category import Category


class VerifyResponse(Base):
    user_id: Union[UUID, str] = Field(alias="userId")
    question_id: Union[UUID, str] = Field(alias="questionId")
    value: str

class UsersQuestions(Base):
    teacher: Teacher
    subject: Subject
    categories: List[Category]