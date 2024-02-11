from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.enums.discipline_types import DisciplineTypes
from app.services.types.base import Base


class NumericEventInfo(Base):
    number: int = Field(alias="number")
    event_info: Optional[str] = Field(alias="eventInfo")


class CertainEvent(Base):
    period: str
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")
    url: Optional[str]
    name: str
    discipline_type: DisciplineTypes = Field(alias="type")
    event_infos: List[NumericEventInfo] = Field(alias="eventInfos")
