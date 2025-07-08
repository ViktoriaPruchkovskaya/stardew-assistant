import asyncio
from contextlib import asynccontextmanager

from api import router
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from persistences.ioc import PersistenceContainer
from services.ioc import ServiceContainer

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with PersistenceContainer() as persistence:
        services = ServiceContainer(persistence)
        await services.start()
        app.state.persistence = persistence
        app.state.services = services

        yield
        await services.shutdown()


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
