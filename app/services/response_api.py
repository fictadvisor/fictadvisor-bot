from typing import Dict, Any
from uuid import UUID

from app.services.base_api import BaseAPI


class ResponseAPI(BaseAPI):
    _path = "/disciplineTeachers"

    async def verify_response(self, response_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
        async with self._session.post(f"{self.path}/{response_id}/responses", json=data) as response:
            return await response.json()
