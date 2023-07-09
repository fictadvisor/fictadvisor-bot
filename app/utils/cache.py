from uuid import uuid4

from cachetools import TTLCache


class AuthCache(TTLCache):
    def __missing__(self, key):
        self[key] = uuid4()
        return self[key]
