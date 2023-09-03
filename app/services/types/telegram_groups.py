from typing import List

from pydantic import BaseModel

from app.services.types.teleram_group import TelegramGroup


class TelegramGroups(BaseModel):
    groups: List[TelegramGroup]
