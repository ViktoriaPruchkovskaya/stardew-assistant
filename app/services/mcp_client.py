from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

from agents import Agent, ModelSettings, Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled
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
    role: Literal["user", "assistant", "system"]  # "user" or "assistant"
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
            instructions="You answer Stardew Valley questions. Reply with a gist.",
            model_settings=ModelSettings(tool_choice="required"),
            mcp_servers=[self.server],
        )
        return self

    async def shutdown(self):
        await self.server.__aexit__(None, None, None)
        return self

    async def process_query(self, context: list[Message]) -> str:
        """Process a query using OpenAI and available MCP tools"""
        result = await Runner.run(self.agent, context)
        return result.final_output

    async def summarize_context(self, context: str) -> str:
        summarize_agent = Agent(
            name="Summarizer",
            instructions=(
                "Summarize prior Stardew chat into compact memory.\n"
                "Output exactly these sections:\n"
                "1) Assistant facts: key factual answers only.\n"
                "2) User intent/constraints: preferences, goals, corrections.\n"
                "3) Open threads: unanswered or pending items.\n"
                "4) Important entities: item names, NPCs, seasons, places.\n"
                "Keep it concise, max ~180 words."
            ),
        )
        result = await Runner.run(summarize_agent, context)
        return result.final_output
