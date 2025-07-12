import os
from typing import Optional

from persistences.ioc import PersistenceContainer

from services.chat_service import ChatService
from services.mcp_client import Config, MCPClient


class ServiceContainer:
    def __init__(self, persistence: PersistenceContainer):
        self.persistence = persistence
        self.mcp_client: Optional[MCPClient] = None
        self.chat_service: Optional[ChatService] = None

    async def start(self):
        await self.get_mcp_client()
        await self.get_chat_service()

    async def get_mcp_client(self) -> MCPClient:
        if self.mcp_client is None:
            config: Config = Config(
                version=os.getenv("API_VERSION"),
                endpoint=os.getenv("ENDPOINT"),
                api_key=os.getenv("SUBSCRIPTION_KEY"),
                deployment=os.getenv("DEPLOYMENT"),
            )
            client = MCPClient(config)
            await client.connect("mcp_tools/wiki_processor.py")
            self.mcp_client = client
        return self.mcp_client

    async def get_chat_service(self) -> ChatService:
        if self.chat_service is None:
            self.chat_service = ChatService(self.persistence.cached_repository, self.mcp_client)
        return self.chat_service

    async def shutdown(self):
        if self.mcp_client:
            await self.mcp_client.shutdown()
