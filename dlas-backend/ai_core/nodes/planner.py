from ai_core.state import GraphState
from langchain_core.messages import  AIMessage

class WorkflowPlanner:

    def run(self, state: GraphState):

        procurement = state["procurement"]

        workflow = []

        if procurement.vendor is None:
            workflow.append({
                    "step":"vendor_search",
                    "status":"pending"
                })

        workflow.extend(
            [   
                {
                    "step": "rfq_generation", 
                    "status": "pending"
                 },
                {
                    "step":"send_rfq",
                    "status":"pending"
                },
                                {
                    "step":"quotation_collection",
                    "status":"pending"
                },                {
                    "step":"quotation_comparison",
                    "status":"pending"
                },                {
                    "step":"recommendation",
                    "status":"pending"
                }
            ]
        )

        return {
            "workflow": workflow,
                "messages": [
                    AIMessage(
                        content="Great! I have collected all the required information. I'll now search for suitable vendors and start the procurement workflow."
                    )
                ]

        }