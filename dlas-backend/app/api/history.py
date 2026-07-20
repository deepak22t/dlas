from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.task_service import TaskService
from app.schemas.chat import HistoryResponse
from app.models.tenant import User
from app.api.deps import get_current_user
history_router = APIRouter()

@history_router.get("/history", response_model=HistoryResponse)
def handle_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_service = TaskService(db)
    return chat_service.get_history(user=current_user)