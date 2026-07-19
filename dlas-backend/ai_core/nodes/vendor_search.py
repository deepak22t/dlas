from ai_core.state import GraphState
from ai_core.services.vendor_service import VendorService
from ai_core.helper.workflow import update_workflow_status
from langchain_core.messages import  AIMessage

class VendorSearchAgent:

    def __init__(self):
        self.service = VendorService()
    
    def run(self, state: GraphState):

        procurement = state["procurement"]

        vendors = self.service.search(procurement)

        vendor_list = "\n".join(
            f"• {vendor.name} ({vendor.city})"
            for vendor in vendors
        )

        message = (
            f"Found {len(vendors)} matching vendor(s).\n\n"
            f"Vendors:\n"
            f"{vendor_list}\n\n"
            "Proceeding to create RFQ."
        )
        workflow = update_workflow_status(

            state["workflow"],

            "vendor_search",

         )   
        return {
            "vendors": vendors,
            "workflow": workflow,
            "messages": [
                AIMessage(content=message)
            ],
        }