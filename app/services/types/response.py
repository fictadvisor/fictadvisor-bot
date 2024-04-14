from typing import List, Union
from uuid import UUID

from pydantic import Field

from app.services.types.answer import Answer
from app.services.types.base import Base
from app.services.types.category import Category
from app.services.types.general_event import Subject
from app.services.types.teacher import Teacher


class VerifyResponse(Base):
    user_id: Union[UUID, str] = Field(alias="userId")
    question_id: Union[UUID, str] = Field(alias="questionId")
    value: str

class UsersQuestions(Base):
    teacher: Teacher
    subject: Subject
    categories: List[Category]

class UsersAnswers(Base):
    answers: List[Answer]
    user_id: Union[UUID, str] = Field(alias="userId")
