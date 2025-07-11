from dataclasses import dataclass

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


class MCPClient:
    def __init__(self, config: Config):

        self.client = AsyncAzureOpenAI(
            api_version=config.version,
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            azure_deployment=config.deployment,
        )
        self.context: list[ResponseInputItemParam] = []
        self.agent: Agent | None = None

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

    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available MCP tools"""
        request = {"role": "user", "content": query}
        self.context.append(request)
        result = await Runner.run(self.agent, self.context)
        response = {"role": "assistant", "content": result.final_output}
        self.context.append(response)
        await self.prune_context()
        return result.final_output

    async def prune_context(self):
        """Keep in the context only the last user-assistant messages, summarize the rest"""
        MAX_TURNS = 6  # pairs of query-response
        TOTAL = MAX_TURNS * 2
        if len(self.context) < TOTAL * 2:
            return
        # 1. extract the summary if any
        summary = None
        if (
            self.context
            and self.context[0]["role"] == "assistant"
            and "Summary of earlier conversation" in self.context[0]["content"]
        ):
            summary = self.context.pop(0)["content"]

        # 2. split context into old and recent
        old_context = self.context[:TOTAL]  # all except last N turns
        recent_context = self.context[TOTAL:]  # last N turns intact

        # 3. assemble old messages into text
        summary_context = summary + "\n" if summary else ""
        summary_context += "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in old_context)

        # 4. summarize assembled messages
        summarize_agent = Agent(
            name="Summarizer",
            instructions="Summarize the earlier user-assistant conversation concisely within Stardew Valley topic. Focus only on asnwers",
        )
        result = await Runner.run(summarize_agent, summary_context)
        summary_text = result.final_output
        self.context = [
            {"role": "assistant", "content": f"Summary of earlier conversation:\n{summary_text}"}
        ] + recent_context
