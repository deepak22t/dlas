# app/services/workflow_step_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.workflow_step import WorkflowStep
from app.models.tenant import User

class WorkflowStepService:
    def __init__(self, db: Session):
        self.db = db

    def save_steps_from_state(self, user: User, task_id: UUID, workflow_list: list) -> None:
        if not workflow_list:
            return

        for index, item in enumerate(workflow_list):
            step_name = item.get("step", "unknown_step")
            step_status = item.get("status", "pending")

            # Check karo ki kya is task ka ye specific step pehle se saved hai?
            existing_step = self.db.query(WorkflowStep).filter(
                WorkflowStep.task_id == task_id,
                WorkflowStep.step_name == step_name
            ).first()

            if existing_step:
                # Agar pehle se hai, toh bas status update kar do
                existing_step.status = step_status
            else:
                # Naya step create karo aur order number assign karo (1, 2, 3...)
                new_step = WorkflowStep(
                    tenant_id=user.tenant_id,
                    user_id=user.id,
                    task_id=task_id,
                    step_name=step_name,
                    status=step_status,
                    step_order=index + 1
                )
                self.db.add(new_step)

        self.db.commit()