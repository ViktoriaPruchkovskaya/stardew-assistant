from dataclasses import asdict, dataclass
from typing import List, TypedDict
from persistences.mongo_db import MongoDB
from persistences.redis import RedisCache
from datetime import datetime
from uuid import uuid4
import json


class Metadata(TypedDict):
    created_at: str


class CreatedRecord(Metadata, total=False):
    _id: str


class CachedRepository:
    def __init__(self, db: MongoDB, cache: RedisCache):
        self._db: MongoDB = db
        self._cache: RedisCache = cache

    async def create_record(self, collection: str, data: dict) -> CreatedRecord:
        id = str(uuid4())
        created_at = datetime.now().isoformat()
        extended_data = data.copy()
        extended_data.update({"_id": id, "created_at": created_at})

        await self._db.insert_one(collection, extended_data)
        self.set_metadata(collection=collection, id=id, data={"created_at": created_at})

        return CreatedRecord(**extended_data)

    def set_metadata(self, collection, id, data: dict):
        self._cache.set(f"{collection}:{id}:metadata", json.dumps(data))

    async def get_metadata(self, collection: str, id: str) -> Metadata:
        cached_record = self._cache.get(f"{collection}:{id}:metadata")
        if cached_record:
            parsed = json.loads(cached_record)
            return Metadata(**parsed)
        selection = {field: 1 for field in Metadata.__annotations__.keys()}
        stored_values = await self._db.get("chats", id, selection)
        if not stored_values:
            raise Exception("No metadata found")
        stored_values.pop("_id", None)
        self.set_metadata(collection, id, stored_values)
        return Metadata(**stored_values)

    async def get_list(self, collection: str, id: str, list_name: str):
        values = self._cache.get_list(f"{collection}:{id}:{list_name}", 0, -1)
        if values:
            return [json.loads(value) for value in values]

        stored_record = await self._db.get(collection, id, {list_name: 1})
        if not stored_record:
            raise Exception("Could not find record")
        if not stored_record[list_name]:
            return []

        self._cache.push(f"{collection}:{id}:{list_name}", [json.dumps(item) for item in stored_record[list_name]])
        return stored_record[list_name]

    async def append_list(self, collection: str, id: str, list_name: str, values: list[dict]):
        await self._db.update_one("chats", id, {"$push": {list_name: {"$each": values}}})
        self._cache.push(f"{collection}:{id}:{list_name}", [json.dumps(value) for value in values])
