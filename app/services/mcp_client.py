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
            instructions=(
                "You are a Stardew Valley assistant.\n"
                "Use conversation memory and user preferences from context. Avoid mentioning game name\n"
                "Workflow:\n"
                "1) For factual gameplay questions, call search_pages_vector with the user's question first.\n"
                "2) Use tool evidence as the primary source of truth for factual claims.\n"
                "3) For follow-up questions with implicit references (for example, pronouns), resolve them from conversation memory.\n"
                "4) Answer with the gist only: 1-3 short bullets, max 70 words total, unless the user asks for more detail.\n"
                "5) Apply user preferences and constraints when formatting and prioritizing the answer.\n"
                "6) If evidence is missing or conflicting, say so briefly and ask one clarifying question.\n"
            ),
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
        # usage = result.context_wrapper.usage
        # print("Requests:", usage.requests)
        # print("Input tokens:", usage.input_tokens)
        # print("Output tokens:", usage.output_tokens)
        # print("Total tokens:", usage.total_tokens)
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
