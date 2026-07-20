import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import UUID, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from sqlalchemy.orm import relationship




class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus,name="task_status"),
        default=TaskStatus.CREATED,
        nullable=False,
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
    
    requirements = relationship(
    "Requirement",
    back_populates="task",
    cascade="all, delete-orphan",
    )

    messages = relationship(
    "Message",
    back_populates="task",
    cascade="all, delete-orphan",
    order_by="Message.created_at",
    )
