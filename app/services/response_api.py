from typing import Union, Dict
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.response import VerifyResponse, UsersQuestions


class ResponseAPI(BaseAPI):
    _path = "/disciplineTeachers"

    async def verify_response(
            self,
            discipline_teacher_id: Union[UUID, str],
            data: VerifyResponse
    ) -> None:
        async with self._session.post(
                f"{self.path}/{discipline_teacher_id}/responses",
                json=data.model_dump(mode="json", by_alias=True)
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                raise ResponseException.from_json(json)

    async def get_users_questions(
        self,
        discipline_teacher_id,
        user_id
    ) -> UsersQuestions:
        params: Dict[str, Union[int, str]] = {"user_id": user_id}
        async with self._session.get(
            f"{self.path}/{discipline_teacher_id}/questions/telegram",
            params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return UsersQuestions.model_validate(json)
            raise ResponseException.from_json(json)
