from dataclasses import asdict, dataclass
from datetime import datetime

from services.mcp_client import MCPClient
from persistences.cached_repository import CachedRepository


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str


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
    def __init__(self, repository: CachedRepository, mcp_client: MCPClient):
        self.mcp_client = mcp_client
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
        summary = await self.repository.get_summary("chats", chat_id)
        prompt_context: list[Message] = (
            [{"role": "system", "content": f"Conversation memory:\n{summary}"}] if summary else []
        )

        recent_messages = await self._get_messages(chat_id)
        prompt_context.extend(recent_messages)
        query = {"role": "user", "content": message}
        prompt_context.append(query)
        result = await self.mcp_client.process_query(prompt_context)

        updated_messages = recent_messages + [query, {"role": "assistant", "content": result}]
        MAX_TURNS = 6  # pairs of query-response
        TOTAL = MAX_TURNS * 2

        if len(updated_messages) < TOTAL * 2:
            await self.append_messages(
                chat_id, [Message(role="user", content=message), Message(role="assistant", content=result)]
            )
            return result
        # 1. split context into old and recent
        old_context = updated_messages[:TOTAL]  # all except last N turns
        recent_context = updated_messages[TOTAL:]  # last N turns intact
        # 2. merge previous summary with old_context before re-summarizing
        prev_summary = f"Previous summary:\n{summary}\n\n" if summary else ""
        turns_block = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in old_context)
        summary_context = (
            f"{prev_summary}"
            "Conversation turns to compress.\n"
            "Preserve user constraints and assistant factual conclusions.\n"
            f"{turns_block}"
        )

        summarized_context = await self.mcp_client.summarize_context(summary_context)

        await self.repository.modify_list(
            collection="chats",
            id=chat_id,
            list_name="messages",
            items=recent_context,
            quantity=len(recent_context),
            other_properties={"summary": summarized_context},
        )
        return result

    async def append_messages(self, chat_id: str, messages: list[Message]):
        messages_dicts = [asdict(msg) for msg in messages]
        await self.repository.append_list(collection="chats", id=chat_id, list_name="messages", values=messages_dicts)

    async def _get_messages(self, chat_id: str) -> list[dict]:
        messages = await self.repository.get_list("chats", chat_id, "messages")
        return [message for message in messages]
