from typing import Optional

import aiohttp
from pydantic import AnyUrl
from yarl import URL

from app.settings import settings


class BaseApi:
    _url: AnyUrl = settings.API_URL
    _path: Optional[str] = None
    _base_url: Optional[URL] = None

    def __init__(self):
        print("base_url", self.base_url)
        self._session = aiohttp.ClientSession(self.base_url, headers=self.get_headers())

    @property
    def base_url(self):
        if self._base_url is None:
            self._base_url = URL(f"{self._url}")

        return self._base_url

    @property
    def path(self):
        return self._base_url.path + self._path

    async def __aenter__(self) -> "BaseApi":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()

    @staticmethod
    def get_headers():
        return {
            "Authorization": f"Token {settings.TOKEN.get_secret_value()}"
        }
