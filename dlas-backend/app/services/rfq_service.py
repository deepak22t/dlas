# app/services/rfq_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.rfq import RFQ
from app.models.tenant import User

class RFQService:
    def __init__(self, db: Session):
        self.db = db

    def save_rfq_from_state(
        self,
        user: User,
        task_id: UUID,
        rfq_state: any  # Ye LangGraph ke state se aane wala RFQ object hoga
    ) -> RFQ | None:
        if not rfq_state:
            return None

        # Check karo agar is task ke liye pehle se RFQ bana hua hai toh update karenge
        existing_rfq = self.db.query(RFQ).filter(RFQ.task_id == task_id).first()

        if existing_rfq:
            existing_rfq.item = getattr(rfq_state, 'item', existing_rfq.item)
            existing_rfq.brand = getattr(rfq_state, 'brand', existing_rfq.brand)
            existing_rfq.quantity = getattr(rfq_state, 'quantity', existing_rfq.quantity)
            existing_rfq.budget = getattr(rfq_state, 'budget', existing_rfq.budget)
            existing_rfq.status = getattr(rfq_state, 'status', existing_rfq.status)
            self.db.commit()
            self.db.refresh(existing_rfq)
            return existing_rfq

        # Agar pehle se nahi hai, toh naya RFQ create karenge
        new_rfq = RFQ(
            tenant_id=user.tenant_id,
            user_id=user.id,
            task_id=task_id,
            item=getattr(rfq_state, 'item', "Unknown Item"),
            brand=getattr(rfq_state, 'brand', None),
            quantity=getattr(rfq_state, 'quantity', 0),
            budget=getattr(rfq_state, 'budget', None),
            status=getattr(rfq_state, 'status', "draft"),
        )

        self.db.add(new_rfq)
        self.db.commit()
        self.db.refresh(new_rfq)
        return new_rfq