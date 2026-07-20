import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import (
    UUID,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class RequirementStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    RFQ_GENERATED = "rfq_generated"
    COMPLETED = "completed"


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    item: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    brand: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    budget: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    delivery_date: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[RequirementStatus] = mapped_column(
        SQLEnum(
            RequirementStatus,
            name="requirement_status",
        ),
        default=RequirementStatus.DRAFT,
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

    task = relationship(
        "Task",
        back_populates="requirements",
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"),
        nullable=False, index=True
        )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"),
          nullable=False
        )