import os
from typing import Optional

from pymongo import MongoClient

from persistences.cache import Cache
from persistences.cached_repository import CachedRepository
from persistences.database import Database
from langgraph.checkpoint.mongodb.saver import MongoDBSaver


class PersistenceContainer:
    def __init__(self):
        self._db: Optional[Database] = None
        self._cache: Optional[Cache] = None
        self.cached_repository: Optional[CachedRepository] = None
        self.checkpointer: Optional[MongoDBSaver] = None

    async def __aenter__(self) -> "PersistenceContainer":
        self._db = PersistenceContainer.init_db()
        await self._db.ping()

        self._cache = Cache(os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PASSWORD"))
        self.cached_repository = CachedRepository(self._db, self._cache)
        conn = MongoClient(self.db_connection_string())
        self.checkpointer = MongoDBSaver(conn)
        return self

    @staticmethod
    def init_db() -> Database:
        return Database(PersistenceContainer.db_connection_string(), os.getenv("DB_NAME"))

    @staticmethod
    def db_connection_string() -> str:
        return f"mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST", "localhost")}:27017/"

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._db:
            self._db.client.close()
        if self._cache:
            self._cache.redis.quit()
        if self.checkpointer:
            self.checkpointer.close()
