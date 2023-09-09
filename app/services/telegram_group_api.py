from typing import Union
from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.telegram_groups import TelegramGroups
from app.services.types.teleram_group import (
    CreateTelegramGroup,
    TelegramGroup,
    UpdateTelegramGroup,
)


class TelegramGroupAPI(BaseAPI):
    _path = "telegramGroups"

    async def create(self, group_id: Union[UUID, str], create_telegram_group: CreateTelegramGroup) -> TelegramGroup:
        async with self._session.post(
                f"{self.path}/{group_id}",
                json=create_telegram_group.model_dump(mode="json", by_alias=True)
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 201:
                return TelegramGroup.model_validate(json)
            raise ResponseException.from_json(json)

    async def update(self, group_id: Union[UUID, str], telegram_id: int, update_telegram_group: UpdateTelegramGroup) -> TelegramGroup:
        async with self._session.patch(
                f"{self.path}",
                params={"telegramId": telegram_id, "groupId": group_id},
                json=update_telegram_group.model_dump(mode="json", by_alias=True)
        ) as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return TelegramGroup.model_validate(json)
            raise ResponseException.from_json(json)

    async def delete(self, group_id: Union[UUID, str], telegram_id: int) -> None:
        async with self._session.delete(
                f"{self.path}",
                params={"telegramId": telegram_id, "groupId": group_id}
        ) as response:
            json = await response.json(content_type=None)
            if response.status != 200:
                raise ResponseException.from_json(json)

    async def get_telegram_groups(self, group_id: Union[UUID, str]) -> TelegramGroups:
        async with self._session.get(f"{self.path}/{group_id}") as response:
            json = await response.json(content_type=None)
            if response.status == 200:
                return TelegramGroups.model_validate(json)
            raise ResponseException.from_json(json)
