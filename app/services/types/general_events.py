from typing import List

from pydantic import BaseModel

from app.services.types.general_event import GeneralEvent


class GeneralEvents(BaseModel):
    events: List[GeneralEvent]
