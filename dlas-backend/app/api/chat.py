from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.chat_service import  create_chat_task
from app.core.config import get_settings



settings = get_settings()
chat_router = APIRouter()

@chat_router.post("/chat", status_code=202)
def handle_chat(request: ChatRequest):
 response = create_chat_task(request.text)
 return response