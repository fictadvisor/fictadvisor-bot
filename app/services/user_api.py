from typing import Any, Dict
from uuid import UUID

from app.enums.state import State
from app.services.base_api import BaseAPI


class UserAPI(BaseAPI):
    _path = "/users"

    async def verify_student(self, student_id: UUID, state: State, is_captain: bool) -> Dict[str, Any]:
        async with self._session.patch(f"{self.path}/{student_id}/verifyStudent",
                                       json={"state": state, "isCaptain": is_captain}) as response:
            return await response.json(content_type=None)

    async def verify_superhero(self, student_id: UUID, state: State) -> Dict[str, Any]:
        async with self._session.patch(f"{self.path}/{student_id}/verifyStudent",
                                       json={"state": state}) as response:
            return await response.json(content_type=None)

    async def get_user(self, user_id: UUID) -> Dict[str, Any]:
        async with self._session.get(f"{self.path}/{user_id}/telegram") as response:
            return await response.json(content_type=None)
