from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel

from services.ioc import ServiceContainer

router = APIRouter(prefix="/chat", tags=["chat"])


def get_services(request: Request) -> ServiceContainer:
    return request.app.state.services


class ChatRequest(BaseModel):
    message: str


@router.get("/{chat_id}")
async def get_chat(chat_id: str, services: ServiceContainer = Depends(get_services)):
    try:
        chat = await services.chat_service.get_chat(chat_id)
        return chat
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{chat_id}")
async def send_message(chat_id: str, data: ChatRequest, services: ServiceContainer = Depends(get_services)):
    res = await services.chat_service.process_message(chat_id, data.message)
    return {"message": res}


@router.post("/")
async def create_chat(services: ServiceContainer = Depends(get_services)):
    res = await services.chat_service.create_chat()
    return {"_id": res}
