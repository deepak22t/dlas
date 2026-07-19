from dataclasses import dataclass


@dataclass
class Recommendation:

    vendor_id: str
    vendor_name: str

    total_score: float

    quoted_amount: float

    budget: float

    savings: float

    decision: str

    reasons: list[str]


class RecommendationService:

    def recommend(

        self,

        comparison,

        quotations,

        budget,

    ):

        best = comparison[0]

        quotation = next(

            q

            for q in quotations

            if q.vendor_id == best.vendor_id

        )

        reasons = []

        reasons.append(
            "Highest overall comparison score."
        )

        if quotation.total_price <= budget:

            reasons.append(
                "Quotation is within budget."
            )

        else:

            reasons.append(
                "Quotation exceeds budget."
            )

        if quotation.delivery_days <= 5:

            reasons.append(
                "Fast delivery."
            )

        if quotation.warranty.startswith("2"):

            reasons.append(
                "Extended warranty."
            )

        if quotation.stock_available:

            reasons.append(
                "Item available in stock."
            )

        savings = budget - quotation.total_price

        if savings >= 0:

            decision = "Recommended for Procurement"

        else:

            decision = "Requires Budget Approval"

        return Recommendation(

            vendor_id=best.vendor_id,

            vendor_name=best.vendor_name,

            total_score=best.total_score,

            quoted_amount=quotation.total_price,

            budget=budget,

            savings=savings,

            decision=decision,

            reasons=reasons,

        )