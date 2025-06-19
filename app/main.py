import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from services.mcp_client import Config, MCPClient
from api import router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    config: Config = Config(
        version=os.getenv("API_VERSION"),
        endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("SUBSCRIPTION_KEY"),
        deployment=os.getenv("DEPLOYMENT"),
    )
    client = MCPClient(config)
    await client.connect("./app/mcp_tools/wiki_processor.py")
    app.state.client = client
    yield
    await client.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")


async def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
