import os
from typing import Optional

from persistences.ioc import PersistenceContainer

from services.chat_service import ChatService
from services.query_service import Config, QueryService


class ServiceContainer:
    def __init__(self, persistence: PersistenceContainer):
        self.persistence = persistence
        self.query_service: Optional[QueryService] = None
        self.chat_service: Optional[ChatService] = None

    async def start(self):
        await self.get_query_service()
        await self.get_chat_service()

    async def get_query_service(self) -> QueryService:
        if self.query_service is None:
            config: Config = Config(
                version=os.getenv("API_VERSION"),
                endpoint=os.getenv("ENDPOINT"),
                api_key=os.getenv("SUBSCRIPTION_KEY"),
                deployment=os.getenv("DEPLOYMENT"),
            )
            self.query_service = QueryService(config, self.persistence.checkpointer)
        return self.query_service

    async def get_chat_service(self) -> ChatService:
        if self.chat_service is None:
            self.chat_service = ChatService(self.persistence.cached_repository, self.query_service)
        return self.chat_service
