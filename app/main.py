import asyncio
import os
from contextlib import asynccontextmanager

from api import router
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from persistences.mongo_db import MongoDB
from services.container import IOCContainer
from services.mcp_client import Config, MCPClient

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection_string = f"mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@localhost:27017/"
    db = MongoDB(connection_string, os.getenv("DB_NAME"))
    config: Config = Config(
        version=os.getenv("API_VERSION"),
        endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("SUBSCRIPTION_KEY"),
        deployment=os.getenv("DEPLOYMENT"),
    )
    client = MCPClient(config, db)
    await client.connect("mcp_tools/wiki_processor.py")

    app.state.services = IOCContainer(mcp_client_service=client)
    yield
    await client.shutdown()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")


async def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
