from openai import AsyncAzureOpenAI
from agents.mcp.server import MCPServerStdio
from dataclasses import dataclass
from agents import Agent, Runner, set_default_openai_client, set_default_openai_api, set_tracing_disabled

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
            azure_deployment=config.deployment
            )
        set_default_openai_api("chat_completions")
        set_default_openai_client(self.client)
        set_tracing_disabled(True)
        
    async def connect(self,  server_script_path: str):
        async with MCPServerStdio(
             params={
                "command":"uv",
                "args": ["run", server_script_path]
            }
        ) as server:
            agent = Agent(
                name="Assistant",
                instructions="You are a helpful assistant which answers stardew valley questions",
                mcp_servers=[server]
            )
            await self.chat_loop(agent)
            
        
    async def process_query(self, agent: Agent,query: str) -> str:
        """Process a query using OpenAI and available MCP tools"""
        result = await Runner.run(agent, query)
        return result.final_output
    
    async def chat_loop(self, agent: Agent):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(agent, query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")