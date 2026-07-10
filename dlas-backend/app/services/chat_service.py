from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.chat import (
    ChatResponse,
    HistoryItem,
    HistoryResponse,
)
from worker.tasks import process_chat_task


def create_chat_task(db: Session, text: str) -> ChatResponse:
    task = Task(
        text=text,
        status="created",
    )

    try:
        db.add(task)
        db.commit()
        db.refresh(task)

        # Send task to Celery worker
        process_chat_task.delay(
            task_id=str(task.id),
            text=task.text,
        )

    except Exception:
        db.rollback()
        raise

    return ChatResponse(
        task_id=str(task.id),
        status=task.status,
    )


def get_history(db: Session) -> HistoryResponse:
    tasks = (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .all()
    )

    return HistoryResponse(
        history=[
            HistoryItem(
                task_id=str(task.id),
                text=task.text,
                status=task.status,
                created_at=task.created_at,
                result=task.result,
            )
            for task in tasks
        ]
    )