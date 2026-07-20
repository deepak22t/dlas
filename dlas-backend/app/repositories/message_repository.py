from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.message import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        message: Message,
    ) -> Message:

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_by_task(
        self,
        task_id,
    ):

        stmt = (
            select(Message)
            .where(Message.task_id == task_id)
            .order_by(Message.created_at)
        )

        return list(self.db.scalars(stmt).all())