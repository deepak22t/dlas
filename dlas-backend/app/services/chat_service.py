from sqlalchemy.orm import Session
from app.schemas.chat import ChatResponse, HistoryResponse, HistoryItem
from app.models.task import Task

def create_chat_task(db: Session, text: str) -> ChatResponse:
    task = Task(
        text=text,
        status="created"
    )
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except:
        db.rollback()
        raise
    
    return ChatResponse(
        task_id=str(task.id),
        status=task.status
    )

def get_history(db: Session) -> HistoryResponse:   
    tasks = (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .all()
)
    return HistoryResponse(
        history=[HistoryItem(
            task_id=str(task.id),
            text=task.text,
            status=task.status,
            created_at=task.created_at
        ) for task in tasks]
    )