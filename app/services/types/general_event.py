from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, Field

from app.services.types.general_discipline_type import GeneralDisciplineType


class GeneralEvent(BaseModel):
    id: Union[UUID, str]
    name: str
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    discipline_type: GeneralDisciplineType = Field(alias="disciplineType")
