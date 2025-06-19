from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


@router.get("/")
def read_root():
    return {"Message": "Hello World! FastAPI is working."}


@router.post("/")
async def get_info(data: ChatRequest, req: Request):
    res = await req.app.state.client.process_query(data.message)
    return {"Message": res}
