from typing import List, TypeVar, Union
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
id = Union[str | ObjectId]


class MongoDB:
    def __init__(self, connection_string: str, db_name: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.connection = self.client[db_name]

    async def ping(self):
        self.client.admin.command("ping")

    async def insert_one(self, collection_name: str, document: any) -> str:
        collection = self.connection[collection_name]
        result = await collection.insert_one(document)
        return result.inserted_id

    async def insert_many(self, collection_name: str, documents: List) -> List[str]:
        collection = self.connection[collection_name]
        result = await collection.insert_many(documents)
        return result.inserted_ids

    async def get(self, collection_name: str, document_id: id, model: type[T]) -> T | None:
        collection = self.connection[collection_name]
        result = await collection.find_one({"_id": document_id})
        if result is None:
            return None
        result["_id"] = str(result["_id"])

        return result

    async def update_one(self, collection_name: str, document_id: id, query: dict) -> int:
        collection = self.connection[collection_name]
        result = await collection.update_one({"_id": document_id}, query)
        return result.modified_count

    async def close(self):
        await self.client.close()
