from typing import Any, Awaitable, Callable, Dict, MutableMapping, Optional

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject, User
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    RATE_LIMIT = 0.7

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self._cache: MutableMapping[int, None] = TTLCache(
            maxsize=10_000, ttl=rate_limit
        )

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self._cache:
                return None

            self._cache[user.id] = None

        try:
            return await handler(event, data)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                return None

            raise
