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


@router.post("/")
async def send_message(data: ChatRequest, services: ServiceContainer = Depends(get_services)):
    res = await services._mcp_client.process_query(data.message)
    return {"message": res}
