from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.groups import GroupsWithTelegramGroup


class GroupAPI(BaseAPI):
    _path = "/groups"

    async def get_groups_with_telegram_groups(self) -> GroupsWithTelegramGroup:
        async with self._session.get(f"{self.path}/telegram/groups") as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return GroupsWithTelegramGroup.model_validate(json)
            raise ResponseException.from_json(json)
