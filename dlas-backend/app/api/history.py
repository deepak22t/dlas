
from fastapi import APIRouter
from app.services.chat_service import get_history

history_router = APIRouter()

@history_router.get("/history")
def handle_history():
 response = get_history()
 return response