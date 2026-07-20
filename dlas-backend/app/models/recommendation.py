# app/models/recommendation.py
import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.database.base import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    rfq_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfqs.id"), nullable=False)
    
    vendor_id: Mapped[str] = mapped_column(String, nullable=False)
    vendor_name: Mapped[str] = mapped_column(String, nullable=False)
    total_score: Mapped[float] = mapped_column(Float, nullable=False)
    quoted_amount: Mapped[float] = mapped_column(Float, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=True)
    savings: Mapped[float] = mapped_column(Float, nullable=True)
    decision: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "Requires Budget Approval"
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)