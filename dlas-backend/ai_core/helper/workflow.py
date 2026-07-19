def update_workflow_status(workflow, completed_step):

    updated = []

    for step in workflow:

        step = step.copy()

        if step["step"] == completed_step:
            step["status"] = "completed"

        updated.append(step)

    return updated