from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(Task).where(Task.id == task_id)
        return self.db.scalar(stmt)

    def list(self) -> list[Task]:
        stmt = select(Task).order_by(Task.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_status(
        self,
        task_id: UUID,
        status: TaskStatus,
    ) -> Task | None:

        task = self.get_by_id(task_id)

        if task is None:
            return None

        task.status = status

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete(self, task_id: UUID) -> bool:

        task = self.get_by_id(task_id)

        if task is None:
            return False

        self.db.delete(task)
        self.db.commit()

        return True