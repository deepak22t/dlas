from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.chat import ChatRequest
from app.services.chat_service import create_chat_task

settings = get_settings()

chat_router = APIRouter()


@chat_router.post("/chat", status_code=202)
def handle_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    response = create_chat_task(db, request.text)
    return response