from dataclasses import dataclass
from typing import Optional, TypedDict

from agents import Agent, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled
from agents.mcp.server import MCPServerStdio
from openai import AsyncAzureOpenAI
from openai.types.responses import ResponseInputItemParam


@dataclass
class Config:
    version: str
    endpoint: str
    api_key: str
    deployment: str


class Message(TypedDict):
    role: str  # "user" or "assistant"
    content: str


class MCPClient:
    def __init__(self, config: Config):

        self.client = AsyncAzureOpenAI(
            api_version=config.version,
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            azure_deployment=config.deployment,
        )
        self.context: list[ResponseInputItemParam] = []
        self.agent: Optional[Agent] = None

        set_default_openai_api("chat_completions")
        set_default_openai_client(self.client)
        set_tracing_disabled(True)

    async def connect(self, server_script_path: str):
        self.server = MCPServerStdio(params={"command": "uv", "args": ["run", server_script_path]})
        await self.server.__aenter__()

        self.agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant which answers Stardew Valley questions. Reply very conciesly.",
            mcp_servers=[self.server],
        )
        return self

    async def shutdown(self):
        await self.server.__aexit__(None, None, None)
        return self

    async def process_query(self, context: dict[Message]) -> str:
        """Process a query using OpenAI and available MCP tools"""
        result = await Runner.run(self.agent, context)
        return result.final_output

    async def summarize_context(self, context: str) -> str:
        summarize_agent = Agent(
            name="Summarizer",
            instructions="Summarize the earlier user-assistant conversation concisely within Stardew Valley topic. Focus only on asnwers",
        )
        result = await Runner.run(summarize_agent, context)
        return result.final_output
