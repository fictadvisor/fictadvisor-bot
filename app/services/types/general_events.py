from typing import List

from pydantic import Field

from app.services.types.base import Base
from app.services.types.general_event import GeneralEvent


class GeneralEvents(Base):
    events: List[GeneralEvent]


class FortnightGeneralEvents(Base):
    first_week_events: List[GeneralEvent] = Field(alias="firstWeekEvents")
    second_week_events: List[GeneralEvent] = Field(alias="secondWeekEvents")
