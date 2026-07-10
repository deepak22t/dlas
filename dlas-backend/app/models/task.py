import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import UUID, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class TaskStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus,name="task_status"),
        default=TaskStatus.CREATED,
        nullable=False,
    )

    result: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
