from fastapi import APIRouter
from app.core.config import get_settings
from app.services.task_service import get_history

settings = get_settings()

router = APIRouter()

@router.get("/")
def handle_root():
 return {"message": f"{settings.app_name} Running"}

