from uuid import UUID, uuid4

from cachetools import TTLCache


class AuthCache(TTLCache[int, UUID]):
    def __missing__(self, key: int) -> UUID:
        self[key] = uuid4()
        return self[key]


cache = AuthCache(maxsize=1000, ttl=60*60)
