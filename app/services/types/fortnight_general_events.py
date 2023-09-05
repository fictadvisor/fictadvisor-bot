from typing import List

from pydantic import BaseModel, Field

from app.services.types.general_event import GeneralEvent


class FortnightGeneralEvents(BaseModel):
    first_week_events: List[GeneralEvent] = Field(alias="firstWeekEvents")
    second_week_events: List[GeneralEvent] = Field(alias="secondWeekEvents")
