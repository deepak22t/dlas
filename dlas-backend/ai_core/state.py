from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from langgraph.checkpoint.postgres import PostgresSaver
from app.core.config import get_settings

settings = get_settings()

class GraphState(TypedDict):
    task_id: str
    messages: Annotated[list[AnyMessage], add_messages]


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