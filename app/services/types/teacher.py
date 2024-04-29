from typing import Optional, Union
from uuid import UUID

from pydantic import Field

from app.services.types.base import Base


class Teacher(Base):
    id: Union[UUID, str]
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    middle_name: Optional[str] = Field(alias="middleName")
