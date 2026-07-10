from fastapi import APIRouter

from app.api.chat import chat_router
from app.api.history import history_router
from app.api.health import health_router

api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(history_router)
api_router.include_router(health_router)