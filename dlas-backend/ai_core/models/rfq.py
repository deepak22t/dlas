from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel

from ai_core.models.vendor import Vendor


class RFQ(BaseModel):

    id: str

    item: str

    brand: str | None

    quantity: int

    budget: float

    specifications: list[str]

    vendors: list[Vendor]

    status: str

    created_at: datetime


    @classmethod
    def create(
        cls,
        procurement,
        vendors,
    ):

        return cls(

            id=str(uuid4()),

            item=procurement.item,

            brand=procurement.brand,

            quantity=procurement.quantity,

            budget=procurement.budget,

            specifications=procurement.specifications,

            vendors=vendors,

            status="draft",

            created_at=datetime.utcnow(),

        )



class RFQDelivery(BaseModel):
    vendor_id: str
    vendor_name: str
    status: str
    sent_at: datetime