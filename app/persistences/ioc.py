import os

from .mongo_db import MongoDB
from .redis import RedisCache
from .cached_repository import CachedRepository


class PersistenceContainer:
    def __init__(self):
        self._mongo: MongoDB | None = None
        self._redis: RedisCache | None = None
        self.cached_repository: CachedRepository | None = None

    async def __aenter__(self) -> "PersistenceContainer":
        self._mongo = self.init_db()
        await self._mongo.ping()

        self._redis = RedisCache(os.getenv("REDIS_PASSWORD"))
        self.cached_repository = CachedRepository(self._mongo, self._redis)

        return self

    def init_db(self) -> MongoDB:
        connection_string = f"mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@localhost:27017/"
        return MongoDB(connection_string, os.getenv("DB_NAME"))

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._mongo:
            self._mongo.client.close()
        if self._redis:
            self._redis.redis.quit()
