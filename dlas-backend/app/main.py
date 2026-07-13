from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import get_settings
from app.database.health import check_database_connection
from ai_core.state import get_postgres_checkpointer

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
        
        check_database_connection()
        print("✔ PostgreSQL Connected")
        with get_postgres_checkpointer() as checkpointer:
            checkpointer.setup()
        print("✔ LangGraph tables created.")
        yield

       
app = FastAPI(title=settings.app_name, lifespan=lifespan, debug=settings.debug)    
app.include_router(api_router)
