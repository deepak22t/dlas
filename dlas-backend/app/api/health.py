from fastapi import APIRouter
from app.core.config import get_settings

settings = get_settings()

health_router = APIRouter()

@health_router.get("/health")
def handle_health():
 return {"message": f"{settings.app_name} Healthy"}