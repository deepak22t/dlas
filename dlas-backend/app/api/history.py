from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.chat_service import get_history

history_router = APIRouter()

@history_router.get("/history")
def handle_history(db: Session = Depends(get_db)):
    response = get_history(db)
    return response