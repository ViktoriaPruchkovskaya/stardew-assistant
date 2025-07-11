from dataclasses import asdict, dataclass
from datetime import datetime

from persistences.cached_repository import CachedRepository


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
    def __init__(self, repository: CachedRepository):
        self.repository = repository

    async def create_chat(self) -> str:
        chat = await self.repository.create_record(collection="chats", data={"messages": []})
        return chat["_id"]

    async def get_chat(self, chat_id: str) -> Chat:
        metadata = await self.repository.get_metadata("chats", chat_id)
        messages = await self.repository.get_list("chats", chat_id, "messages")
        return Chat(_id=chat_id, messages=messages, created_at=metadata["created_at"])

    async def append_messages(self, chat_id: str, messages: list[Message]):
        messages_dicts = [asdict(msg) for msg in messages]
        await self.repository.append_list(collection="chats", id=chat_id, list_name="messages", values=messages_dicts)
