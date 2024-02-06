from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import Field

from app.enums.discipline_types import DisciplineTypes
from app.services.types.base import Base


class GeneralEvent(Base):
    id: Union[UUID, str]
    name: str
    url: Optional[str]
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    discipline_type: DisciplineTypes = Field(alias="eventType")
