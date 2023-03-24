from enum import Enum
from typing import Any, Dict
from uuid import UUID

from app.services.base_api import BaseAPI


class State(str, Enum):
    PENDING = "PENDING"
    APPROVED = 'APPROVED'
    DECLINED = 'DECLINED'


class UserAPI(BaseAPI):
    _path = "/users"

    async def verify_student(self, student_id: UUID, state: State, is_captain: bool) -> Dict[str, Any]:
        async with self._session.patch(f"{self.path}/{student_id}/verifyStudent",
                                       json={"state": state, "isCaptain": is_captain}) as response:
            return await response.json()

    async def verify_superhero(self, student_id: UUID, state: State, is_captain: bool) -> Dict[str, Any]:
        async with self._session.patch(f"{self.path}/{student_id}/verifyStudent",
                                       json={"state": state, "isCaptain": is_captain}) as response:
            return await response.json()

    async def get_user(self, user_id: UUID) -> Dict[str, Any]:
        async with self._session.get(f"{self.path}/{user_id}/telegram") as response:
            return await response.json()
