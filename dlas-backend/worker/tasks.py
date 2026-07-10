import time

from app.database.session import SessionLocal
from app.models.task import Task
from app.models.task import TaskStatus
from worker.celery_app import celery
from ai_core.ai_service import AIService

ai_service = AIService()

@celery.task(name="process_chat_task")
def process_chat_task(task_id: str, text: str) -> str:
    """
    Process a chat request in the background.
    """

    db = SessionLocal()

    try:
        task = db.get(Task, task_id)

        if task is None:
            return "Task not found"

        # Mark task as processing
        task.status = TaskStatus.PROCESSING
        db.commit()

        # Simulate long-running work
        #time.sleep(5)

        # Dummy output (LLM response will replace this later)
        result = ai_service.generate_response(text)

        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()

        return result

    except Exception as exc:
        db.rollback()

        if task is not None:
            task.status = TaskStatus.FAILED
            db.commit()

        raise

    finally:
        db.close()