# app/services/recommendation_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation
from app.models.tenant import User

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def save_recommendation_from_state(
        self, 
        user: User, 
        task_id: UUID, 
        rfq_id: UUID, 
        rec_state: any
    ) -> Recommendation | None:
        if not rec_state or not rfq_id:
            return None

        existing_rec = self.db.query(Recommendation).filter(Recommendation.task_id == task_id).first()

        if existing_rec:
            existing_rec.vendor_id = str(getattr(rec_state, 'vendor_id', existing_rec.vendor_id))
            existing_rec.vendor_name = getattr(rec_state, 'vendor_name', existing_rec.vendor_name)
            existing_rec.total_score = float(getattr(rec_state, 'total_score', existing_rec.total_score))
            existing_rec.quoted_amount = float(getattr(rec_state, 'quoted_amount', existing_rec.quoted_amount))
            existing_rec.budget = getattr(rec_state, 'budget', existing_rec.budget)
            existing_rec.savings = getattr(rec_state, 'savings', existing_rec.savings)
            existing_rec.decision = getattr(rec_state, 'decision', existing_rec.decision)
            self.db.commit()
            self.db.refresh(existing_rec)
            return existing_rec

        new_rec = Recommendation(
            tenant_id=user.tenant_id,
            user_id=user.id,
            task_id=task_id,
            rfq_id=rfq_id,
            vendor_id=str(getattr(rec_state, 'vendor_id', '')),
            vendor_name=getattr(rec_state, 'vendor_name', 'Unknown Vendor'),
            total_score=float(getattr(rec_state, 'total_score', 0.0)),
            quoted_amount=float(getattr(rec_state, 'quoted_amount', 0.0)),
            budget=getattr(rec_state, 'budget', None),
            savings=getattr(rec_state, 'savings', None),
            decision=getattr(rec_state, 'decision', 'Pending')
        )
        self.db.add(new_rec)
        self.db.commit()
        self.db.refresh(new_rec)
        return new_rec