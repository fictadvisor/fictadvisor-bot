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


class VerifyEvent(Base):
    week: int
    name: Optional[str]
    disciplineId: Optional[Union[UUID, str]]
    eventType: Optional[DisciplineTypes]
    teachers: Optional[List[Teacher]]
    start_time: Optional[datetime] = Field(alias="startTime")
    changeStartDate: Optional[bool] = False
    end_time: Optional[datetime] = Field(alias="endTime")
    period: Optional[EventPeriod]
    url: Optional[str]
    event_info: Optional[str] = Field(alias="eventInfo")
    disciplineInfo: Optional[str] = Field(alias="discipline_info")
