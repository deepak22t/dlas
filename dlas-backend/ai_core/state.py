from typing import Annotated, Literal, Optional
from langgraph.checkpoint import serde
from pydantic import BaseModel,Field
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from langgraph.checkpoint.postgres import PostgresSaver
from app.core.config import get_settings
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from ai_core.models.rfq import RFQ ,RFQDelivery
from ai_core.models.quotation import VendorQuotation
# Inhe allowlist mein directly tuple list ki tarah pass karo jaisa warning bol rahi hai
from ai_core.models.quotation import VendorComparison
from ai_core.services.recommendation_service import Recommendation
my_serde = JsonPlusSerializer(
    allowed_msgpack_modules=[
        ("ai_core.state", "ProcurementEntities"),
        ("ai_core.state", "ProcurementState")
    ]
)
settings = get_settings()



class Vendor(BaseModel):
    id: str
    name: str
    city: str
    rating: float
    brands: list[str]

class RequirementValidation(BaseModel):

    complete: bool = False

    missing_fields: list[str] = Field(default_factory=list)


class ProcurementEntities(BaseModel):

    item: Optional[str] = None

    brand: Optional[str] = None

    quantity: Optional[int] = None

    budget: Optional[float] = None

    vendor: Optional[str] = None

    specifications: list[str] = []

    delivery_date: Optional[str] = None


class ProcurementState(BaseModel):

    item: str | None = None

    brand: str | None = None

    quantity: int | None = None

    budget: float | None = None

    vendor: str | None = None

    specifications: list[str] = []

    delivery_date: str | None = None

class GraphState(TypedDict):

    task_id: str

    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]

    intent: Literal[
        "general_chat",
        "procurement",
    ]
    confidence: float
    entities: ProcurementEntities | None
    procurement: ProcurementState | None
    validation: RequirementValidation | None
    workflow: list[str]
    vendors: list[Vendor] = []
    rfq: RFQ | None = None
    quotations: list[VendorQuotation]
    deliveries: list[RFQDelivery]
    comparison: list[VendorComparison]

    recommendation: Recommendation | None
    reasoning: str


class IntentDecision(BaseModel):
    intent: Literal[
        "general_chat",
        "procurement",
    ]
    confidence: float
    reasoning: str






_pool = None
def get_pool():
    global _pool

    if _pool is None:
        _pool = ConnectionPool(
            conninfo=settings.database_url,
            max_size=10,
            min_size=2,
            kwargs={"autocommit": True},
        )
    return _pool


@contextmanager
def get_postgres_checkpointer():
    with get_pool().connection() as conn:
        checkpointer = PostgresSaver(conn,serde=my_serde)
        yield checkpointer