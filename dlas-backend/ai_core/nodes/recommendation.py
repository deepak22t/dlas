from langchain_core.messages import AIMessage

from ai_core.helper.workflow import update_workflow_status

from ai_core.services.recommendation_service import RecommendationService


class RecommendationAgent:

    def __init__(self):

        self.service = RecommendationService()

    def run(

        self,

        state,

    ):

        recommendation = self.service.recommend(

            comparison=state["comparison"],

            quotations=state["quotations"],

            budget=state["rfq"].budget,

        )

        workflow = update_workflow_status(

            state["workflow"],

            "recommendation",

        )

        if recommendation.savings >= 0:

            savings = f"₹{recommendation.savings:,.0f}"

        else:

            savings = f"-₹{abs(recommendation.savings):,.0f}"

        reason_text = "\n".join(

            f"✓ {reason}"

            for reason in recommendation.reasons

        )

        message = (

            "===============================\n"

            "PROCUREMENT RECOMMENDATION\n"

            "===============================\n\n"

            f"Recommended Vendor : {recommendation.vendor_name}\n\n"

            f"Overall Score : {recommendation.total_score:.2f}/100\n\n"

            "Reasons\n"

            "-------\n"

            f"{reason_text}\n\n"

            "Financial Summary\n"

            "-----------------\n"

            f"Budget : ₹{recommendation.budget:,.0f}\n"

            f"Quotation : ₹{recommendation.quoted_amount:,.0f}\n"

            f"Savings : {savings}\n\n"

            f"Decision : {recommendation.decision}\n\n"

            "Workflow Status\n"

            "---------------\n"

            "✓ Vendor Search\n"

            "✓ RFQ Generation\n"

            "✓ Send RFQ\n"

            "✓ Quotation Collection\n"

            "✓ Quotation Comparison\n"

            "✓ Recommendation\n\n"

            "Procurement workflow completed."

        )

        return {

            "recommendation": recommendation,

            "workflow": workflow,

            "messages": [

                AIMessage(

                    content=message,

                )

            ],

        }