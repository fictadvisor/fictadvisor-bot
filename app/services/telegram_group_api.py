from uuid import UUID

from app.services.base_api import BaseAPI
from app.services.types.create_telegram_group import CreateTelegramGroup


class TelegramGroupAPI(BaseAPI):
    _path = "telegramGroups"

    async def create(self, group_id: UUID, create_telegram_group: CreateTelegramGroup):
        async with self._session.post(f"{self.path}/{group_id}", json=create_telegram_group.model_dump(by_alias=True)) as response:
            return await response.json(content_type=None)
