from dataclasses import dataclass
from datetime import datetime
from services.query_service import QueryService, Message
from persistences.cached_repository import CachedRepository


@dataclass
class Chat:
    _id: str
    created_at: datetime
    messages: list[Message]


@dataclass
class CreatedChat:
    _id: str
    created_at: str


class ChatService:
    def __init__(self, repository: CachedRepository, query_service: QueryService):
        self.query_service = query_service
        self.repository = repository

    async def create_chat(self) -> CreatedChat:
        chat = await self.repository.create_record(collection="chats", data={"messages": [], "summary": ""})
        return CreatedChat(_id=chat["_id"], created_at=chat["created_at"])

    async def get_chat(self, chat_id: str) -> Chat:
        metadata = await self.repository.get_metadata("chats", chat_id)
        messages = await self._get_messages(chat_id)
        return Chat(_id=chat_id, messages=messages, created_at=metadata["created_at"])

    async def delete_chats(self, chat_ids: list[str]):
        await self.repository.delete_many("chats", chat_ids)
        self.repository.delete_metadata("chats", chat_ids)

    async def process_message(self, chat_id: str, message: str) -> str:
        result = await self.query_service.process_query(chat_id, message)
        await self.append_messages(
            chat_id, [Message(role="user", content=message), Message(role="assistant", content=result)]
        )
        return result

    async def append_messages(self, chat_id: str, messages: list[Message]):
        await self.repository.append_list(collection="chats", id=chat_id, list_name="messages", values=messages)

    async def _get_messages(self, chat_id: str) -> list[dict]:
        messages = await self.repository.get_list("chats", chat_id, "messages")
        return [message for message in messages]
