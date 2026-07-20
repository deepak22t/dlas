from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tenant import User
from app.models.requirement import (
    Requirement,
    RequirementStatus,
)
from app.repositories.requirement_repository import (
    RequirementRepository,
)


class RequirementService:

    def __init__(self, db: Session):
        self.repository = RequirementRepository(db)

    def save_requirement(
        self,
        user: User,          # <-- NEW: User object accept karo
        task_id: UUID,
        item: str | None,
        brand: str | None = None,
        quantity: int | None = None,
        budget: float | None = None,
        delivery_date: str | None = None,
    ) -> Requirement:

        # Check whether a requirement already exists for this task
        requirement = self.repository.get_by_task_id(task_id)

        # -----------------------------------
        # Update existing requirement
        # -----------------------------------
        if requirement:
            if item is not None:
                requirement.item = item
            if brand is not None:
                requirement.brand = brand
            if quantity is not None:
                requirement.quantity = quantity
            if budget is not None:
                requirement.budget = budget
            if delivery_date is not None:
                requirement.delivery_date = delivery_date

            # Note: Update karte waqt tenant/user change nahi hote, isliye ye same rahega
            return self.repository.update(requirement)

        # -----------------------------------
        # Create new requirement
        # -----------------------------------
        requirement = Requirement(
            task_id=task_id,
            tenant_id=user.tenant_id,  # <-- NEW: Tenant ID bind ho gaya
            user_id=user.id,           # <-- NEW: User ID bind ho gaya
            item=item,
            brand=brand,
            quantity=quantity,
            budget=budget,
            delivery_date=delivery_date,
            status=RequirementStatus.DRAFT,
        )

        return self.repository.create(requirement)
    def get_requirement(
        self,
        requirement_id: UUID,
    ) -> Requirement | None:

        return self.repository.get_by_id(requirement_id)

    def get_task_requirement(
        self,
        task_id: UUID,
    ) -> Requirement | None:

        return self.repository.get_by_task_id(task_id)

    def get_all_requirements(self, user: User) -> list[Requirement]:
        return self.repository.list_by_tenant(tenant_id=user.tenant_id)

    def update_requirement_status(
        self,
        requirement_id: UUID,
        status: RequirementStatus,
    ) -> Requirement | None:

        return self.repository.update_status(
            requirement_id,
            status,
        )

    def delete_requirement(
        self,
        requirement_id: UUID,
    ) -> bool:

        return self.repository.delete(requirement_id)