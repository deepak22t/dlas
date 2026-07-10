import uuid
from app.schemas.chat import ChatResponse, HistoryResponse

def create_chat_task(text: str) -> ChatResponse:
    task_id = _generate_task_id()
    return ChatResponse(
        task_id=task_id,
        status="created"
    )

def _generate_task_id():
    return str(uuid.uuid4())

def get_history() -> HistoryResponse:
    return HistoryResponse(
        history=["Hello, I am a chatbot"],
        status="completed" 
    )