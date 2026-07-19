from langchain_core.messages import AIMessage

from ai_core.services.rfq_service import RFQService,RFQDelivery
from ai_core.state import GraphState
from ai_core.helper.workflow import update_workflow_status
from datetime import datetime




class RFQGenerator:

    def __init__(self):

        self.service = RFQService()

    def run(
        self,
        state: GraphState,
    ):

        procurement = state["procurement"]

        vendors = state["vendors"]

        rfq = self.service.create(

            procurement=procurement,

            vendors=vendors,

        )

        vendor_names = ", ".join(
            vendor.name
            for vendor in vendors
        )

        summary = (
            "RFQ Summary\n\n"
            f"Product : {rfq.item}\n"
            f"Brand : {rfq.brand or 'Any'}\n"
            f"Quantity : {rfq.quantity}\n"
            f"Budget : ₹{rfq.budget:,.0f}\n"
            f"Vendor : {vendor_names}\n\n"
            f"Status : {rfq.status.title()}"
        )
        workflow = update_workflow_status(

            state["workflow"],

            "rfq_generation",

        )
        return {
            "rfq": rfq,
            "workflow": workflow,
            "messages": [
                AIMessage(content=summary)
            ]
        }
class SendRFQAgent:

    def run(self, state: GraphState):

        rfq = state["rfq"]

        deliveries = []

        for vendor in rfq.vendors:

            deliveries.append(

                RFQDelivery(

                    vendor_id=vendor.id,
                    vendor_name=vendor.name,
                    status="sent",
                    sent_at=datetime.utcnow(),

                )

            )

        rfq.status = "sent"

        vendor_status = "\n".join(

            f"✓ {delivery.vendor_name}\n"
            f"Status : {delivery.status.title()}\n"
            f"Time : {delivery.sent_at.strftime('%I:%M %p')}"

            for delivery in deliveries

        )
        workflow = update_workflow_status(

            state["workflow"],

            "send_rfq",

        )
        message = (
            "RFQ dispatched.\n\n"
            "Vendor Status\n\n"
            f"{vendor_status}"
        )

        return {

            "rfq": rfq,
            "workflow": workflow,
            "deliveries": deliveries,

            "messages": [

                AIMessage(content=message)

            ],

        }