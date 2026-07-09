from fastapi import FastAPI
from app.api.chat import chat_router
from app.api.history import history_router
from app.api.health import health_router
from app.core.config import get_settings
    
settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)    
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(health_router)

