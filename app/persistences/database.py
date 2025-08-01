from typing import List, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

id = Union[str | ObjectId]


class Database:
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

    async def get(self, collection_name: str, document_id: id, options: dict = {}):
        collection = self.connection[collection_name]
        result = await collection.find_one({"_id": document_id}, options)
        if result is None:
            return None
        result["_id"] = str(result["_id"])

        return result

    async def delete_many(self, collection_name: str, document_ids: list[id]):
        collection = self.connection[collection_name]
        collection.delete_many({"_id": {"$in": document_ids}})

    async def update_one(self, collection_name: str, document_id: id, query: dict) -> int:
        collection = self.connection[collection_name]
        result = await collection.update_one({"_id": document_id}, query)
        return result.modified_count
