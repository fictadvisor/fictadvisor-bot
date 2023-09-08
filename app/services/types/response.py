from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field


class VerifyResponse(BaseModel):
    user_id: Union[UUID, str] = Field(serialization_alias="userId")
    question_id: Union[UUID, str] = Field(serialization_alias="questionId")
    value: str
