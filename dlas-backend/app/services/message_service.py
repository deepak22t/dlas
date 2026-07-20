from uuid import UUID
from sqlalchemy.orm import Session
from app.models.message import Message
from app.repositories.message_repository import MessageRepository


class MessageService:

    def __init__(self, db: Session):
        self.repository = MessageRepository(db)

    def add_message(
        self,
        task_id: UUID,
        role: str,
        content: str,
        tenant_id: UUID,
        user_id: UUID,
    ) -> Message:
        message = Message(
            task_id=task_id,
            role=role,
            content=content,
            tenant_id=tenant_id,
            user_id=user_id,
        )
        return self.repository.create(message)

    def get_messages_by_task(
        self,
        task_id: UUID,
        tenant_id: UUID,
    ) -> list[Message]:
        return self.repository.list_by_task_and_tenant(task_id, tenant_id)