import os

from .mongo_db import MongoDB


class PersistenceContainer:
    def __init__(self):
        self._mongo: MongoDB | None = None

    async def __aenter__(self) -> MongoDB:
        connection_string = f"mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@localhost:27017/"
        self._mongo = MongoDB(connection_string, os.getenv("DB_NAME"))
        await self._mongo.ping()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._mongo:
            self._mongo.client.close()
