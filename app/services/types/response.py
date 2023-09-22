from typing import Union
from uuid import UUID

from pydantic import Field

from app.services.types.base import Base


class VerifyResponse(Base):
    user_id: Union[UUID, str] = Field(alias="userId")
    question_id: Union[UUID, str] = Field(alias="questionId")
    value: str
