from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.chat import ChatRequest
from app.services.task_service import TaskService
settings = get_settings()

chat_router = APIRouter()


@chat_router.post("/chat", status_code=202)
def handle_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):   
    service = TaskService(db)
    print("Incoming task_id:", request.task_id)
    print("Incoming text:", request.text)
    return service.create_chat_task(
    text=request.text,
    task_id=request.task_id,
)