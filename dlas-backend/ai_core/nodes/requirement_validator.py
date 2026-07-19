from ai_core.state import (
    GraphState,
    RequirementValidation,
)


class RequirementValidator:

    REQUIRED_FIELDS = [

        "item",
        "quantity",
        "budget",

    ]

    def run(self, state: GraphState):

        procurement = state["procurement"]

        missing = []

        for field in self.REQUIRED_FIELDS:

            value = getattr(procurement, field)

            if value is None:

                missing.append(field)

        return RequirementValidation(

            complete=len(missing) == 0,

            missing_fields=missing,

        )