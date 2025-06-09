import asyncio
from dotenv import load_dotenv
import os
load_dotenv()
from server.mcp_client import MCPClient, Config
            

async def main():
    config: Config = Config(
        version=os.getenv("API_VERSION"),
        endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("SUBSCRIPTION_KEY"),
        deployment=os.getenv("DEPLOYMENT")
        )
    client = MCPClient(config)
    await client.connect("./mcp/main.py")
        
if __name__ == "__main__":
    asyncio.run(main())
