from typing import Union
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.student import Student, VerifyStudent


class UserAPI(BaseAPI):
    _path = "/users"

    async def verify_student(self, student_id: Union[UUID, str], data: VerifyStudent) -> None:
        async with self._session.patch(
                f"{self.path}/{student_id}/verifyStudent",
                json=data.model_dump(mode="json", by_alias=True)
        ) as response:
            json = await response.json(content_type=None)
            if response.status != 200:
                raise ResponseException.from_json(json)

    async def get_user(self, user_id: Union[UUID, str]) -> Student:
        async with self._session.get(f"{self.path}/{user_id}/telegram") as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return Student.model_validate(json)
            raise ResponseException.from_json(json)

    async def get_user_by_telegram_id(self, telegram_id: int) -> Student:
        async with self._session.get(f"{self.path}/telegramUser/{telegram_id}") as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return Student.model_validate(json)
            raise ResponseException.from_json(json)
