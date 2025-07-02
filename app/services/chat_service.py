from persistences.mongo_db import MongoDB


class ChatService:
    def __init__(self, db: MongoDB):
        self.db = db

    async def create_chat(self) -> str:
        return ""
