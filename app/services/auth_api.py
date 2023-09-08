
from app.services.base_api import BaseAPI
from app.services.exceptions.response_exception import ResponseException
from app.services.types.telegram import RegisterTelegram


class AuthAPI(BaseAPI):
    _path = "/auth"

    async def register_telegram(self, data: RegisterTelegram) -> None:
        async with self._session.post(f"{self.path}/registerTelegram", json=data.model_dump(by_alias=True)) as response:
            json = await response.json(content_type=None)
            if response.status != 200:
                raise ResponseException.from_json(json)
