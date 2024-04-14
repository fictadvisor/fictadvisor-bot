from pydantic import Field

from app.services.types.base import Base


class Answer(Base):
    question_id: str = Field(alias="questionId")
    value: str
