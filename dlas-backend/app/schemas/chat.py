from pydantic import BaseModel
from datetime import datetime

class ChatRequest(BaseModel):
 text: str

class ChatResponse(BaseModel):
    task_id: str
    status: str

class HistoryItem(BaseModel):
    task_id: str
    text: str
    status: str
    result: str | None = None
    created_at: datetime | None = None
    
class HistoryResponse(BaseModel):
    history: list[HistoryItem]
