from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.chat import chat_router
from app.api.history import history_router
from app.api.health import health_router
from app.core.config import get_settings
from app.database.health import check_database_connection

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_database_connection()
    yield
    #need to define databse connection close

app = FastAPI(title=settings.app_name, lifespan=lifespan, debug=settings.debug)    
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(health_router)
