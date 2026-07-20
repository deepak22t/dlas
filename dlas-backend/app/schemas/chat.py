from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ChatRequest(BaseModel):
    task_id: UUID | None = None
    text: str

class ChatResponse(BaseModel):
    task_id: str
    response: str
    status: str

class HistoryItem(BaseModel):
    task_id: str
    text: str
    status: str
    created_at: datetime | None = None
    
class HistoryResponse(BaseModel):
    history: list[HistoryItem]
