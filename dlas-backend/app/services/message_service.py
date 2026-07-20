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
    ):

        message = Message(
            task_id=task_id,
            role=role,
            content=content,
        )

        return self.repository.create(message)

    def get_messages(
        self,
        task_id: UUID,
    ):

        return self.repository.get_by_task(task_id)