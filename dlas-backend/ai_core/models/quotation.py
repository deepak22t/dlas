from dataclasses import dataclass


@dataclass
class VendorQuotation:

    vendor_id: str

    vendor_name: str

    unit_price: float

    total_price: float

    delivery_days: int

    warranty: int

    stock_available: bool

    remarks: str


@dataclass
class VendorComparison:

    vendor_id: str

    vendor_name: str

    price_score: float

    delivery_score: float

    warranty_score: float

    rating_score: float

    budget_score: float

    total_score: float

    rank: int