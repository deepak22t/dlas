from langchain_core.messages import AIMessage
from ai_core.services.rfq_service import RFQService
from ai_core.helper.workflow import update_workflow_status
from ai_core.helper.quotation_formatter import build_summary

class QuotationCollectionAgent:

    def __init__(self):

        self.service = RFQService()

    def run(self, state):

        rfq = state["rfq"]

        quotations = self.service.collect_quotations(rfq)

        workflow = update_workflow_status(
            state["workflow"],
            "quotation_collection",
        )

        summary = build_summary(
        state["rfq"],
        quotations,
        )
        return {

            "quotations": quotations,

            "workflow": workflow,

             "messages": [

                    AIMessage(content=summary)

              ]

        }