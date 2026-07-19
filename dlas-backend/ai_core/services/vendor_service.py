from ai_core.repositories.vendor_repository import VendorRepository


class VendorService:

    def __init__(self):
        self.repository = VendorRepository()

    def search(self, procurement):

        return self.repository.search(
            item=procurement.item,
            brand=procurement.brand,
        )