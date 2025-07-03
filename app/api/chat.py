from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel

from persistences.mongo_db import MongoDB
from services.ioc import ServiceContainer

router = APIRouter(prefix="/chat", tags=["chat"])


def get_services(request: Request) -> ServiceContainer:
    return request.app.state.services


class ChatRequest(BaseModel):
    message: str


@router.get("/{chat_id}")
async def get_chat(chat_id: str):
    # chat = await db.get("stardew", chat_id)
    # if not chat:
    #     raise HTTPException(status_code=404, detail="Chat not found")
    # return chat
    return ""


@router.post("/{chat_id}")
async def send_message(chat_id: str, data: ChatRequest, services: ServiceContainer = Depends(get_services)):
    res = await services.mcp_client.process_query(data.message)
    return {"message": res}


@router.post("/")
async def create_chat(services: ServiceContainer = Depends(get_services)):
    res = await services.chat_service.create_chat()
    return {"id": res}
