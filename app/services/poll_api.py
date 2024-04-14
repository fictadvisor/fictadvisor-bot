from typing import Dict, Optional, Union
from uuid import UUID

from app.enums.poll import PollOrder, PollSort
from app.enums.role import TeacherRole
from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.users_teachers import UsersTeachers


class PollAPI(BaseAPI):
    _path = "/poll"

    async def get_users_teachers(
            self,
            user_id: Union[UUID, str],
            search: Optional[str] = None,
            sort: Optional[PollSort]= None,
            order: Optional[PollOrder] = None,
            roles: Optional[TeacherRole] = None
            ) -> UsersTeachers:
        params: Dict[str, Union[int, str]] = {}
        if search:
            params.update({"search": search})
        if sort:
            params.update({"sort": sort})
        if order:
            params.update({"order": order})
        if roles:
            params.update({"roles": roles})
        async with self._session.get(
            f"{self.path}/teachers/{user_id}",
            params=params
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return UsersTeachers.model_validate(json)
            raise ResponseException.from_json(json)
