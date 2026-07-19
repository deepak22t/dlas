from pydantic import BaseModel


class Vendor(BaseModel):
    id: str
    name: str
    city: str
    rating: float
    brands: list[str]