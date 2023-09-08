from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.discipline_types import DisciplineTypes


class GeneralDisciplineType(BaseModel):
    id: Union[UUID, str]
    discipline_id: Union[UUID, str] = Field(alias="disciplineId")
    name: DisciplineTypes
