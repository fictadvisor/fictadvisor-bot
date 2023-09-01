from typing import Any, Dict, Union
from uuid import UUID

from app.services.base_api import BaseAPI


class ResponseAPI(BaseAPI):
    _path = "/disciplineTeachers"

    async def verify_response(
            self,
            discipline_teacher_id: Union[UUID, str],
            user_id: Union[UUID, str],
            question_id: Union[UUID, str],
            value: str
    ) -> Dict[str, Any]:
        async with self._session.post(f"{self.path}/{discipline_teacher_id}/responses", json={
            "userId": str(user_id),
            "questionId": str(question_id),
            "value": value
        }) as response:
            return await response.json()
