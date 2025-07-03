from dataclasses import asdict, dataclass
from persistences.mongo_db import MongoDB
from uuid import uuid4
from datetime import datetime


@dataclass
class Message:
    role: str  # "user" or "assistant"
    text: str


@dataclass
class Chat:
    _id: str
    created_at: datetime
    messages: list[Message]


class ChatService:
    def __init__(self, db: MongoDB):
        self.db = db

    async def create_chat(self) -> str:
        chat_id = str(uuid4())
        await self.db.insert_one("chats", {"_id": chat_id, "messages": [], "created_at": datetime.now()})
        return chat_id

    async def get_chat(self, chat_id: str) -> Chat:
        chat = await self.db.get("chats", chat_id, Chat)
        if chat is None:
            raise Exception("Chat not found")
        return chat

    async def append_messages(self, chat_id: str, messages: list[Message]):
        messages_dicts = [asdict(msg) for msg in messages]
        await self.db.update_one("chats", chat_id, {"$push": {"messages": {"$each": messages_dicts}}})
