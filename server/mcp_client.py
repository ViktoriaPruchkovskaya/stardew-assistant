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
        set_default_openai_api("chat_completions")
        set_default_openai_client(self.client)
        set_tracing_disabled(True)

    async def connect(self, server_script_path: str):
        async with MCPServerStdio(params={"command": "uv", "args": ["run", server_script_path]}) as server:
            agent = Agent(
                name="Assistant",
                instructions="You are a helpful assistant which answers stardew valley questions. Reply very conciesly.",
                mcp_servers=[server],
            )
            await self.chat_loop(agent)

    async def process_query(self, agent: Agent, query: str) -> str:
        """Process a query using OpenAI and available MCP tools"""
        self.context.append({"role": "user", "content": query})
        result = await Runner.run(agent, self.context)
        self.context.append({"role": "assistant", "content": result.final_output})
        await self.prune_context()
        return result.final_output

    async def prune_context(self):
        """Keep in the context only the last user-assistant messages, summarize the rest"""
        MAX_TURNS = 4  # pairs of query-response
        TOTAL = MAX_TURNS * 2
        if len(self.context) < TOTAL * 2:
            return
        old_context = self.context[:TOTAL]  # all except last N turns
        recent_context = self.context[TOTAL:]  # last N turns intact

        old_context_text = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in old_context)
        summarize_agent = Agent(
            name="Summarizer",
            instructions="Summarize the earlier user-assistant conversation concisely. Focus on key topics",
        )
        result = await Runner.run(summarize_agent, old_context_text)
        summary_text = result.final_output
        self.context = [
            {"role": "system", "content": f"Summary of earlier conversation:\n{summary_text}"}
        ] + recent_context

    async def chat_loop(self, agent: Agent):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(agent, query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")
