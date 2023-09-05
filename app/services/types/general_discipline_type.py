from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.discipline_types import DisciplineTypes


class GeneralDisciplineType(BaseModel):
    id: UUID
    discipline_id: UUID = Field(alias="disciplineId")
    name: DisciplineTypes
