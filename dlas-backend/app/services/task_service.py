from uuid import UUID
from sqlalchemy.orm import Session

from ai_core.main import process_task_without_celery
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.persistence.workflow_persistence import WorkflowPersistence
from app.services.message_service import MessageService
from app.schemas.chat import ChatRequest
from app.models.tenant import User
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
        request: ChatRequest,
        user: User
    ) -> ChatResponse:
        try: 
            task = None
            print("Received task_id:", request.task_id)
            if request.task_id:
                task = self.repository.get_by_id(request.task_id)
                print("Task:", task)
            
            if task is None:
                task = Task(
                    status=TaskStatus.CREATED,
                    tenant_id=user.tenant_id,
                    user_id=user.id
                )
                task = self.repository.create(task)                
            
            self.message_service.add_message(
                task_id=task.id,
                role="user",
                content=request.text,
                tenant_id=user.tenant_id,
                user_id=user.id
            )
            
            final_state = process_task_without_celery(
                task_id=task.id,
                user_request=request.text
            )
            
            # Updated: user object pass kar diya gaya hai
            WorkflowPersistence(self.db).persist(
                task_id=task.id,
                state=final_state,
                user=user,
            )
            
            task = self.repository.update_status(
                task.id,
                TaskStatus.COMPLETED,
            )
            
            self.message_service.add_message(
                task_id=task.id,
                role="assistant",
                content=final_state["messages"][-1].content,
                tenant_id=user.tenant_id,  
                user_id=user.id           
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

    def get_history(self, user: User) -> HistoryResponse:
        tasks = self.repository.list_by_tenant(tenant_id=user.tenant_id)

        return HistoryResponse(
            history=[
                HistoryItem(
                    task_id=str(task.id),
                    text=task.user_request if hasattr(task, 'user_request') else "",
                    status=task.status,
                    created_at=task.created_at,
                )
                for task in tasks
            ]
        )

    def get_task(self, task_id: UUID):
        return self.repository.get_by_id(task_id)

    def delete_task(self, task_id: UUID):
        return self.repository.delete(task_id)