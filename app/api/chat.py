from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from services.container import IOCContainer

router = APIRouter(prefix="/chat", tags=["chat"])


def get_services(request: Request) -> IOCContainer:
    return request.app.state.services


class ChatRequest(BaseModel):
    message: str


@router.get("/")
def read_root():
    return {"message": "Hello World! FastAPI is working."}


@router.post("/")
async def get_info(data: ChatRequest, services: IOCContainer = Depends(get_services)):
    res = await services.mcp_client_service.process_query(data.message)
    return {"message": res}
