from persistences.mongo_db import MongoDB
from uuid import uuid4
from datetime import datetime


class ChatService:
    def __init__(self, db: MongoDB):
        self.db = db

    async def create_chat(self) -> str:
        chat_id = str(uuid4())
        await self.db.insert_one("chats", {"_id": chat_id, "messages": [], "created_at": datetime.now()})
        return chat_id
