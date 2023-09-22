from typing import Union
from uuid import UUID

from pydantic import Field

from app.enums.discipline_types import DisciplineTypes
from app.services.types.base import Base


class GeneralDisciplineType(Base):
    id: Union[UUID, str]
    discipline_id: Union[UUID, str] = Field(alias="disciplineId")
    name: DisciplineTypes
