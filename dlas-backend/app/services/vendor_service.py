# app/services/vendor_service.py
from sqlalchemy.orm import Session
from app.models.vendor import Vendor
from app.models.tenant import User

class VendorService:
    def __init__(self, db: Session):
        self.db = db

    def save_vendors_from_state(self, user: User, vendors_state: list) -> list[Vendor]:
        if not vendors_state:
            return []

        saved_vendors = []
        for v in vendors_state:
            vendor_name = getattr(v, 'name', 'Unknown Vendor')
            
            # Check karo ki kya is company (tenant) me ye vendor pehle se saved hai?
            existing_vendor = self.db.query(Vendor).filter(
                Vendor.tenant_id == user.tenant_id,
                Vendor.name == vendor_name
            ).first()

            if existing_vendor:
                # Agar pehle se hai, toh bas rating aur city update kar do
                existing_vendor.city = getattr(v, 'city', existing_vendor.city)
                existing_vendor.rating = float(getattr(v, 'rating', existing_vendor.rating))
                saved_vendors.append(existing_vendor)
            else:
                # Agar naya vendor hai, toh naya row banao (PostgreSQL apna naya UUID generate karega)
                new_vendor = Vendor(
                    tenant_id=user.tenant_id,
                    user_id=user.id,
                    name=vendor_name,
                    city=getattr(v, 'city', None),
                    rating=float(getattr(v, 'rating', 0.0)),
                    is_active=True
                )
                self.db.add(new_vendor)
                saved_vendors.append(new_vendor)

        self.db.commit()
        return saved_vendors