from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.task_service import TaskService

history_router = APIRouter()

@history_router.get("/history")
def handle_history(db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_history()