from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from langgraph.checkpoint.postgres import PostgresSaver
from app.core.config import get_settings
from typing import Annotated, Literal
from pydantic import BaseModel


settings = get_settings()
class ProcurementContext(BaseModel):
    item: str = ""
    quantity: int | None = None
    budget: float | None = None

    vendor: str = ""

    specifications: str = ""

    delivery_date: str = ""

    current_stage: str = "requirement_collection"


class SupervisorDecision(BaseModel):

    next_agent: Literal[
        "negotiator",
        "financial",
        "scraper",
        "rfq",
        "end",
    ]

    workflow: str

    reasoning: str


    ## context
    item: str

    quantity: int | None

    budget: float | None

    vendor: str

    specifications: str

    delivery_date: str

    current_stage: str

class GraphState(TypedDict):
    task_id: str

    messages: Annotated[list[AnyMessage], add_messages]

    next_agent: Literal[
        "negotiator",
        "financial",
        "scraper",
        "rfq",
        "end",
    ]

    context: ProcurementContext

    workflow: str

    supervisor_reasoning: str


pool = ConnectionPool(
    conninfo=settings.database_url,
    max_size=10,
    min_size=2,
    kwargs={"autocommit": True} 
)

@contextmanager
def get_postgres_checkpointer()   :
    """
    Safely yields a checkpointer wrapper bound to an active pool connection.
    Closes the connection context *only* after execution scope exits.
    """
    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        yield checkpointer