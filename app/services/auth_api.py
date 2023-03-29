from typing import Dict, Any, Union
from uuid import UUID

from app.services.base_api import BaseAPI


class AuthAPI(BaseAPI):
    _path = "/auth"

    async def register_telegram(self, token: Union[UUID, str], telegram_id: int) -> Dict[str, Any]:
        async with self._session.post(f"{self.path}/registerTelegram", json={
            "token": str(token),
            "telegramId": str(telegram_id)
        }) as response:
            return await response.json()
