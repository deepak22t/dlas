# app/persistence/workflow_persistence.py ke andar:

from uuid import UUID
from sqlalchemy.orm import Session
from app.models.tenant import User
from app.services.requirement_service import RequirementService
from app.services.rfq_service import RFQService
from app.services.quotation_service import QuotationService
from app.services.recommendation_service import RecommendationService
from app.services.vendor_service import VendorService 
from app.services.workflow_step_service import WorkflowStepService

class WorkflowPersistence:
    def __init__(self, db: Session):
        self.requirement_service = RequirementService(db)
        self.rfq_service = RFQService(db)
        self.quotation_service = QuotationService(db)
        self.recommendation_service = RecommendationService(db)
        self.vendor_service = VendorService(db)
        self.step_service = WorkflowStepService(db) 

    def persist(self, task_id: UUID, state: dict, user: User) -> None:
        procurement = state.get("procurement")

        if procurement is None or procurement.item is None:
            return

        # 1. Save Requirement
        self.requirement_service.save_requirement(
            user=user,
            task_id=task_id,
            item=procurement.item,
            brand=procurement.brand,
            quantity=procurement.quantity,
            budget=procurement.budget,
            delivery_date=procurement.delivery_date,
        )

        # 2. NEW: Save Vendors (RFQ se pehle save karo taaki registry ban jaye)
        vendors_state = state.get("vendors")
        if vendors_state:
            self.vendor_service.save_vendors_from_state(user=user, vendors_state=vendors_state)

        # 3. Save RFQ
        rfq_state = state.get("rfq")
        saved_rfq = None
        if rfq_state:
            saved_rfq = self.rfq_service.save_rfq_from_state(
                user=user,
                task_id=task_id,
                rfq_state=rfq_state
            )

        # 4. Save Quotations
        quotations_state = state.get("quotations")
        if saved_rfq and quotations_state:
            self.quotation_service.save_quotations_from_state(
                user=user,
                rfq_id=saved_rfq.id,
                quotations_state=quotations_state
            )

        # 5. Save Recommendation
        rec_state = state.get("recommendation")
        if saved_rfq and rec_state:
            self.recommendation_service.save_recommendation_from_state(
                user=user,
                task_id=task_id,
                rfq_id=saved_rfq.id,
                rec_state=rec_state
            )

        workflow_list = state.get("workflow")
        if workflow_list:
            self.step_service.save_steps_from_state(user=user, task_id=task_id, workflow_list=workflow_list)