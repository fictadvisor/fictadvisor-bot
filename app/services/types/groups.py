from typing import List

from app.services.types.base import Base
from app.services.types.group import GroupWithTelegramGroupsResponse


class GroupsWithTelegramGroup(Base):
    groups: List[GroupWithTelegramGroupsResponse]
