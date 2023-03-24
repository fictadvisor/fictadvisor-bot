from uuid import UUID

from app.services.base_api import BaseApi


class ResponseApi(BaseApi):
    _path = "/disciplineTeachers"

    async def verify_response(self, response_id: UUID, data):
        async with self._session.post(f"{self.path}/{response_id}/responses", json=data) as response:
            print(response.url)
            return await response.json()
