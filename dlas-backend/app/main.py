from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import get_settings
from app.database.health import check_database_connection

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        check_database_connection()
        print("✔ PostgreSQL Connected")
        yield

    except Exception as e:
        raise e
       

app = FastAPI(title=settings.app_name, lifespan=lifespan, debug=settings.debug)    
app.include_router(api_router)
