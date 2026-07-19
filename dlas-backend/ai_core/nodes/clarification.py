from langchain_core.messages import  AIMessage

FIELD_LABELS = {
    "item": "product",
    "quantity": "quantity",
    "budget": "budget",
    "brand": "preferred brand",
    "vendor": "preferred vendor",
    "delivery_date": "delivery date",
}
class ClarificationAgent:

    def run(self, state):

        validation = state["validation"]

        fields = [
            FIELD_LABELS[field]
            for field in validation.missing_fields
        ]

        content = (
            "I need a little more information.\n\n"
            + "\n".join(
                f"• Please provide {field}."
                for field in fields
            )
        )

        return {
         "messages": [
                    AIMessage(
                        content=content
                    )
                ]
        }