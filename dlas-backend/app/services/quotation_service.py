# app/services/quotation_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.quotation import Quotation
from app.models.tenant import User

class QuotationService:
    def __init__(self, db: Session):
        self.db = db

    def save_quotations_from_state(
        self, 
        user: User, 
        rfq_id: UUID, 
        quotations_state: list
    ) -> None:
        if not quotations_state or not rfq_id:
            return

        for q in quotations_state:
            # Check karte hain ki kya is RFQ aur Vendor ka quote pehle se save toh nahi hai
            vendor_id_str = str(getattr(q, 'vendor_id', ''))
            existing_quote = self.db.query(Quotation).filter(
                Quotation.rfq_id == rfq_id,
                Quotation.vendor_id == vendor_id_str
            ).first()

            if existing_quote:
                existing_quote.unit_price = float(getattr(q, 'unit_price', existing_quote.unit_price))
                existing_quote.total_price = float(getattr(q, 'total_price', existing_quote.total_price))
                existing_quote.delivery_days = getattr(q, 'delivery_days', existing_quote.delivery_days)
                existing_quote.warranty = getattr(q, 'warranty', existing_quote.warranty)
                existing_quote.remarks = getattr(q, 'remarks', existing_quote.remarks)
            else:
                new_quote = Quotation(
                    tenant_id=user.tenant_id,
                    user_id=user.id,
                    rfq_id=rfq_id,
                    vendor_id=vendor_id_str,
                    vendor_name=getattr(q, 'vendor_name', 'Unknown Vendor'),
                    unit_price=float(getattr(q, 'unit_price', 0.0)),
                    total_price=float(getattr(q, 'total_price', 0.0)),
                    delivery_days=getattr(q, 'delivery_days', None),
                    warranty=getattr(q, 'warranty', None),
                    stock_available=getattr(q, 'stock_available', True),
                    remarks=getattr(q, 'remarks', None)
                )
                self.db.add(new_quote)

        self.db.commit()