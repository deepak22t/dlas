# app/models/workflow_step.py
import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base

class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False, index=True)
    
    step_name: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'vendor_search', 'send_rfq'
    status: Mapped[str] = mapped_column(String, default="pending")  # pending, running, completed, failed, waiting_for_approval
    step_order: Mapped[int] = mapped_column(Integer, default=1)     # UI me cards ko line se dikhane ke liye
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)