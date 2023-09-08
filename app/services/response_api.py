from typing import Union
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.response import VerifyResponse


class ResponseAPI(BaseAPI):
    _path = "/disciplineTeachers"

    async def verify_response(
            self,
            discipline_teacher_id: Union[UUID, str],
            data: VerifyResponse
    ) -> None:
        async with self._session.post(f"{self.path}/{discipline_teacher_id}/responses", json=data.model_dump(by_alias=True)) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                raise ResponseException.from_json(json)
