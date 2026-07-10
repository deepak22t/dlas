from pydantic import BaseModel

class ChatRequest(BaseModel):
 text: str

class ChatResponse(BaseModel):
    task_id: str
    status: str

class HistoryItem(BaseModel):
    task_id: str
    text: str
    status: str

class HistoryResponse(BaseModel):
    history: list[HistoryItem]
