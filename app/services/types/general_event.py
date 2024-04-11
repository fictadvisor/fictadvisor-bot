from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import Field

from app.enums.discipline_types import DisciplineTypes
from app.enums.event_period import EventPeriod
from app.services.types.base import Base
from app.services.types.teacher import Teacher


class GeneralEvent(Base):
    id: Union[UUID, str]
    name: str
    url: Optional[str]
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    discipline_type: Optional[DisciplineTypes] = Field(alias="eventType")
    event_info: Optional[str] = Field(alias="eventInfo")

    def __hash__(self) -> int:
        hash_value = 5381
        for char in self.name:
            hash_value = (hash_value * 33) ^ ord(char)
        return hash_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeneralEvent):
            raise NotImplementedError
        return self.id == other.id or (self.name == other.name and self.discipline_type == other.discipline_type)

    def __lt__(self, other: 'GeneralEvent') -> bool:
        return str(self.name).lower() < str(other.name).lower()


class VerifyEvent(Base):
    week: int
    event_info: str = Field(alias="eventInfo")
    name: Optional[str] = None
    disciplineId: Optional[Union[UUID, str]] = None
    eventType: Optional[DisciplineTypes] = None
    teachers: Optional[List[Teacher]] = None
    start_time: Optional[datetime] = None
    changeStartDate: Optional[bool] = False
    end_time: Optional[datetime] = None
    period: Optional[EventPeriod] = None
    url: Optional[str] = None
    disciplineInfo: Optional[str] = None
    discipline_type: DisciplineTypes = Field(alias="eventType")
