from langchain_core.messages import AIMessage

from ai_core.helper.workflow import update_workflow_status
from ai_core.services.comparison_service import ComparisonService
from ai_core.helper.quotation_formatter import build_comparison 

class QuotationComparisonAgent:

    def __init__(self):

        self.service = ComparisonService()

    def run(self, state):

        comparisons = self.service.compare(

            quotations=state["quotations"],

            vendors=state["vendors"],

            budget=state["rfq"].budget,

        )

        workflow = update_workflow_status(

            state["workflow"],

            "quotation_comparison",

        )

        lines = [

            "Quotation Comparison\n"

        ]

        lines=build_comparison(comparisons)
        return {

            "comparison": comparisons,

            "workflow": workflow,

            "messages": [

                AIMessage(

                    content="\n".join(lines)

                )

            ],

        }