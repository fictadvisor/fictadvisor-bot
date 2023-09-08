from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.state import State
from app.services.types.group import ExtendedGroup


class BaseStudent(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    middle_name: Optional[str] = Field(alias="middleName")


class Student(BaseStudent):
    id: Union[UUID, str]
    username: str
    email: str
    avatar: str
    telegram_id: Optional[int] = Field(alias="telegramId")
    group: ExtendedGroup


class VerifyStudent(BaseModel):
    state: State
    is_captain: bool = Field(serialization_alias="isCaptain")
