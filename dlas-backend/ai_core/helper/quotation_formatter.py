def build_summary(rfq, quotations):

    quotation_summary = []

    for quotation in quotations:

        budget_status = (
            "✅ Within Budget"
            if quotation.total_price <= rfq.budget
            else "❌ Budget Exceeded"
        )

        quotation_summary.append(

            f"""
    Vendor : {quotation.vendor_name}

    Unit Price : ₹{quotation.unit_price:,.0f}

    Total Price : ₹{quotation.total_price:,.0f}

    Delivery : {quotation.delivery_days} days

    Warranty : {quotation.warranty}

    Stock :
    {"Available" if quotation.stock_available else "Unavailable"}

    Budget :
    {budget_status}

    Remarks :
    {quotation.remarks}

    ---------------------------------
    """
        )

    message = (
        "Quotation Collection Completed\n\n"
        + "\n".join(quotation_summary)
        + "\nPreparing quotation comparison..."
    )
    return message

def build_comparison(comparisons):
    for comparison in comparisons:
        lines = []
        lines.append(

            f"""
            Rank : {comparison.rank}

            Vendor : {comparison.vendor_name}

            Overall Score : {comparison.total_score:.2f}/100

            Price Score : {comparison.price_score:.2f}

            Delivery Score : {comparison.delivery_score:.2f}

            Warranty Score : {comparison.warranty_score:.2f}

            Vendor Rating Score : {comparison.rating_score:.2f}

            Budget Score : {comparison.budget_score:.2f}

            ----------------------------------------
            """
                        )

        lines.append(

            "Preparing final recommendation..."

        )

        return lines
