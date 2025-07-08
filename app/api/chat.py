from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel

from services.chat_service import Message
from services.ioc import ServiceContainer

router = APIRouter(prefix="/chat", tags=["chat"])


def get_services(request: Request) -> ServiceContainer:
    return request.app.state.services


class ChatRequest(BaseModel):
    message: str


@router.get("/{chat_id}")
async def get_chat(chat_id: str, services: ServiceContainer = Depends(get_services)):
    try:
        chat = services.chat_service.get_chat(chat_id=chat_id)
        return chat
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{chat_id}")
async def send_message(chat_id: str, data: ChatRequest, services: ServiceContainer = Depends(get_services)):
    res = await services.mcp_client.process_query(data.message)
    messages = [Message(role="user", text=data.message), Message(role="assistant", text=res)]
    await services.chat_service.append_messages(chat_id=chat_id, messages=messages)
    return {"message": res}


@router.post("/")
async def create_chat(services: ServiceContainer = Depends(get_services)):
    res = await services.chat_service.create_chat()
    return {"id": res}
