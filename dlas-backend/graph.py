from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import operator

memory = MemorySaver()

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]


def chatbot_node(state: AgentState):
    user_message = state["messages"][-1]
    print(user_message)
    return {"messages": [f"Agent says: {user_message}"]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", chatbot_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)
app_graph = workflow.compile(checkpointer=memory)