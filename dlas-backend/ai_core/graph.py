from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver  # Later replaced by PostgresSaver

from ai_core.agents.supervisor import SupervisorAgent
from ai_core.state import GraphState


supervisor = SupervisorAgent()
saver = MemorySaver()


def supervisor_node(state: GraphState) -> GraphState:
    response = supervisor.run(state["messages"])
    return {"messages": [response]}



builder = StateGraph(GraphState)
builder.add_node("supervisor", supervisor_node)
builder.add_edge(START, "supervisor")
builder.add_edge("supervisor", END)

# Checkpointer apply karke compile karein
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)