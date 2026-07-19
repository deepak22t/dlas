from ai_core.models.quotation import VendorComparison


class ComparisonService:

    PRICE_WEIGHT = 40
    DELIVERY_WEIGHT = 20
    WARRANTY_WEIGHT = 15
    RATING_WEIGHT = 15
    BUDGET_WEIGHT = 10

    def compare(
        self,
        quotations,
        vendors,
        budget,
    ):

        comparisons = []

        min_price = min(q.total_price for q in quotations)
        max_price = max(q.total_price for q in quotations)

        min_delivery = min(q.delivery_days for q in quotations)
        max_delivery = max(q.delivery_days for q in quotations)

        for quotation in quotations:

            vendor = next(
                vendor
                for vendor in vendors
                if vendor.id == quotation.vendor_id
            )

            # -----------------------------
            # Price Score (Lower is Better)
            # -----------------------------

            if max_price == min_price:
                price_score = self.PRICE_WEIGHT
            else:
                price_score = (
                    (max_price - quotation.total_price)
                    /
                    (max_price - min_price)
                ) * self.PRICE_WEIGHT

            # -----------------------------
            # Delivery Score
            # -----------------------------

            if max_delivery == min_delivery:
                delivery_score = self.DELIVERY_WEIGHT
            else:
                delivery_score = (
                    (max_delivery - quotation.delivery_days)
                    /
                    (max_delivery - min_delivery)
                ) * self.DELIVERY_WEIGHT

            # -----------------------------
            # Warranty Score
            # -----------------------------

            if quotation.warranty.startswith("2"):
                warranty_score = self.WARRANTY_WEIGHT

            elif quotation.warranty.startswith("1"):
                warranty_score = self.WARRANTY_WEIGHT * 0.6

            else:
                warranty_score = self.WARRANTY_WEIGHT * 0.3

            # -----------------------------
            # Vendor Rating
            # -----------------------------

            rating_score = (
                vendor.rating / 5
            ) * self.RATING_WEIGHT

            # -----------------------------
            # Budget
            # -----------------------------

            if quotation.total_price <= budget:
                budget_score = self.BUDGET_WEIGHT
            else:
                budget_score = 0

            total_score = (
                price_score
                + delivery_score
                + warranty_score
                + rating_score
                + budget_score
            )

            comparisons.append(

                VendorComparison(

                    vendor_id=vendor.id,

                    vendor_name=vendor.name,

                    price_score=round(price_score, 2),

                    delivery_score=round(delivery_score, 2),

                    warranty_score=round(warranty_score, 2),

                    rating_score=round(rating_score, 2),

                    budget_score=round(budget_score, 2),

                    total_score=round(total_score, 2),

                    rank=0,

                )

            )

        comparisons.sort(

            key=lambda comparison: comparison.total_score,

            reverse=True,

        )

        for rank, comparison in enumerate(

            comparisons,

            start=1,

        ):

            comparison.rank = rank

        return comparisons