from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse, HistoryResponse
from app.services.task_service import TaskService
from app.models.tenant import User
from app.api.deps import get_current_user

settings = get_settings()
chat_router = APIRouter()


@chat_router.post("/chat", response_model=ChatResponse)
def handle_chat(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):  
    chat_service = TaskService(db)
    return chat_service.create_chat_task(request=request, user=current_user)
