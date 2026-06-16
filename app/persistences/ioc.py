import os
from typing import Optional

from pymongo import MongoClient

from persistences.database import Database
from langgraph.checkpoint.mongodb.saver import MongoDBSaver


class PersistenceContainer:
    def __init__(self):
        self.db: Optional[Database] = None
        self.checkpointer: Optional[MongoDBSaver] = None

    async def __aenter__(self) -> "PersistenceContainer":
        self.db = PersistenceContainer.init_db()
        await self.db.ping()

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
        if self.db:
            self.db.client.close()
        if self.checkpointer:
            self.checkpointer.close()
