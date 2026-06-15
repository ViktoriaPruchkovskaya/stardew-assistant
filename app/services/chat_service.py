from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Literal
from uuid import uuid4

from persistences.database import Database
from services.query_service import QueryService

@dataclass
class ChatMessage:
    role: Literal["user", "assistant"]
    content: str
    
@dataclass
class Chat:
    _id: str
    created_at: datetime
    messages: list[ChatMessage]

@dataclass
class CreatedChat:
    _id: str
    created_at: str


class ChatService:
    def __init__(self, repository: Database, query_service: QueryService):
        self.query_service = query_service
        self.repository = repository
        self._collection = "chats"

    async def create_chat(self) -> CreatedChat:
        id = str(uuid4())
        created_at = datetime.now().isoformat()
        record = Chat(_id=id, created_at=created_at, messages=[])
        chat_id = await self.repository.insert_one(self._collection, asdict(record))
        return CreatedChat(_id=chat_id, created_at=created_at)

    async def get_chat(self, chat_id: str) -> Chat:
        chat = await self.repository.get(self._collection, chat_id)
        return Chat(_id=chat_id, messages=chat["messages"], created_at=chat["created_at"])

    async def delete_chats(self, chat_ids: list[str]):
        await self.repository.delete_many("chats", chat_ids)

    async def process_message(self, chat_id: str, message: str) -> str:
        result = await self.query_service.process_query(chat_id, message)
        messages = [{"role":"user", "content":message}, {"role":"assistant", "content":result}]
        await self.repository.update_one(self._collection, chat_id, {"$push": {"messages": {"$each": messages}}})
        return result
