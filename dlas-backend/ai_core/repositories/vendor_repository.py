from ai_core.models.vendor import Vendor


class VendorRepository:

    def search(
        self,
        item: str,
        brand: str | None,
    ) -> list[Vendor]:

        vendors = [

            Vendor(
                id="1",
                name="ABC Electronics",
                city="Delhi",
                rating=4.8,
                brands=["Dell", "HP", "Lenovo"],
            ),

            Vendor(
                id="2",
                name="Tech World",
                city="Mumbai",
                rating=4.5,
                brands=["Apple", "Samsung", "Vivo"],
            ),

            Vendor(
                id="3",
                name="Office Solutions",
                city="Lucknow",
                rating=4.6,
                brands=["HP", "Canon"],
            ),
        ]

        if brand is None:
            return vendors

        return [
            vendor
            for vendor in vendors
            if brand.lower() in map(str.lower, vendor.brands)
        ]