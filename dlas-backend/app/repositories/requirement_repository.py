from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.requirement import (
    Requirement,
    RequirementStatus,
)


class RequirementRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        requirement: Requirement,
    ) -> Requirement:

        self.db.add(requirement)
        self.db.commit()
        self.db.refresh(requirement)

        return requirement

    def get_by_id(
        self,
        requirement_id: UUID,
    ) -> Requirement | None:

        stmt = select(Requirement).where(
            Requirement.id == requirement_id
        )

        return self.db.scalar(stmt)

    def list_all(self) -> list[Requirement]:

        stmt = select(Requirement).order_by(
            Requirement.created_at.desc()
        )

        return list(self.db.scalars(stmt).all())

    def get_by_task_id(
        self,
        task_id: UUID,
    ) -> Requirement | None:

        stmt = (
            select(Requirement)
            .where(Requirement.task_id == task_id)
        )

        return self.db.scalar(stmt)
    def update(
        self,
        requirement: Requirement,
    ) -> Requirement:

        self.db.commit()
        self.db.refresh(requirement)

        return requirement

    def update_status(
        self,
        requirement_id: UUID,
        status: RequirementStatus,
    ) -> Requirement | None:

        requirement = self.get_by_id(requirement_id)

        if requirement is None:
            return None

        requirement.status = status

        self.db.commit()
        self.db.refresh(requirement)

        return requirement

    def delete(
        self,
        requirement_id: UUID,
    ) -> bool:

        requirement = self.get_by_id(requirement_id)

        if requirement is None:
            return False

        self.db.delete(requirement)
        self.db.commit()

        return True