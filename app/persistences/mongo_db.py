from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient


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

    async def get(self, collection_name: str, document_id: str) -> dict:
        collection = self.connection[collection_name]
        result = await collection.find_one({"_id": ObjectId(document_id)})

        result["_id"] = str(result["_id"])

        return result

    async def close(self):
        await self.client.close()
