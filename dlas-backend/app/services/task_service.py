from sqlalchemy.orm import Session

from ai_core.main import process_task_without_celery
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.persistence.workflow_persistence import WorkflowPersistence
from app.services.message_service import MessageService
from app.schemas.chat import (
    ChatResponse,
    HistoryItem,
    HistoryResponse,
)


class TaskService:

    def __init__(self, db: Session):
        self.repository = TaskRepository(db)
        self.message_service = MessageService(db)
        self.db = db
    def create_chat_task(
        self,
        text: str,
        task_id: str | None = None,
    ):
         
        try: 
            task = None
            print("Received task_id:", task_id)
            if task_id:
              task = self.repository.get_by_id(task_id)
              print("Task:", task)
            if task is None:

                task = Task(
                    status=TaskStatus.CREATED,
                )

                task = self.repository.create(task)                
            self.message_service.add_message(
                task.id,
                "user",
                text,
            )
            final_state = process_task_without_celery(
                task_id=task.id,
                user_request=text,
            )
            WorkflowPersistence(self.db).persist(
            task.id,
            final_state,
            )
            task = self.repository.update_status(
                task.id,
                TaskStatus.COMPLETED,
            )
            self.message_service.add_message(
            task.id,
            "assistant",
            final_state["messages"][-1].content,
             )
            return ChatResponse(
                task_id=str(task.id),
                response=final_state["messages"][-1].content,
                status=task.status,
            )

        except Exception:

            self.db.rollback()

            if task is not None:
                self.repository.update_status(
                    task.id,
                    TaskStatus.FAILED,
                )

            raise

    def get_history(self) -> HistoryResponse:

        tasks = self.repository.list()

        return HistoryResponse(
            history=[
                HistoryItem(
                    task_id=str(task.id),
                    text=task.user_request,
                    status=task.status,
                    created_at=task.created_at,
                )
                for task in tasks
            ]
        )

    def get_task(self, task_id):

        return self.repository.get_by_id(task_id)

    def delete_task(self, task_id):

        return self.repository.delete(task_id)