from ai_core.models.rfq import RFQ
from datetime import datetime
from pydantic import BaseModel
from ai_core.models.quotation import VendorQuotation
import random
class RFQService:

    def create(
        self,
        procurement,
        vendors,
    ):

        return RFQ.create(

            procurement=procurement,

            vendors=vendors,

        )
    def collect_quotations(self, rfq):

        remarks_pool = [
            "Ready to Dispatch",
            "OEM Warranty Included",
            "Bulk Discount Available",
            "Limited Stock",
            "Negotiable",
            "In Stock"
        ]

        quotations = []

        for vendor in rfq.vendors:

            unit_price = random.randint(47000, 52000)

            delivery_days = random.randint(2, 10)

            warranty = random.choice(
                [
                    "1 Year",
                    "2 Years"
                ]
            )

            remarks = random.choice(remarks_pool)

            quotation = VendorQuotation(

                vendor_id=vendor.id,

                vendor_name=vendor.name,

                unit_price=unit_price,

                total_price=unit_price * rfq.quantity,

                delivery_days=delivery_days,

                warranty=warranty,

                stock_available=True,

                remarks=remarks,

            )

            quotations.append(quotation)

        return quotations


class RFQDelivery(BaseModel):
    vendor_id: str
    vendor_name: str
    status: str
    sent_at: datetime