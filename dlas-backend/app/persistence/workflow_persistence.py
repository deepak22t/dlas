from sqlalchemy.orm import Session

from app.services.requirement_service import RequirementService


class WorkflowPersistence:

    def __init__(self, db: Session):
        self.requirement_service = RequirementService(db)

    def persist(self, task_id, state) -> None:

        procurement = state.get("procurement")

        # Nothing to persist if procurement state doesn't exist
        if procurement is None:
            return

        # Nothing to persist if no item has been identified yet
        if procurement.item is None:
            return

        self.requirement_service.save_requirement(
            task_id=task_id,
            item=procurement.item,
            brand=procurement.brand,
            quantity=procurement.quantity,
            budget=procurement.budget,
            delivery_date=procurement.delivery_date,
        )

        # Later
        # RFQService.save(...)
        # QuotationService.save(...)
        # RecommendationService.save(...)