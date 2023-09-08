from typing import Union
from uuid import UUID

from pydantic import BaseModel

from app.enums.role import Role
from app.enums.state import State


class Group(BaseModel):
    id: Union[UUID, str]
    code: str


class ExtendedGroup(Group):
    state: State
    role: Role
