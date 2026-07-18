from langgraph.graph import StateGraph, START, END

from ai_core.state import GraphState,ProcurementContext

from ai_core.agents.supervisor import SupervisorAgent
from ai_core.agents.negotiator import NegotiatorAgent
from ai_core.agents.financial import FinancialAgent
from ai_core.agents.scraper import ScraperAgent
from ai_core.agents.rfq import RFQAgent


supervisor = SupervisorAgent()
negotiator = NegotiatorAgent()
financial = FinancialAgent()
scraper = ScraperAgent()
rfq = RFQAgent()


# -----------------------------
# Nodes
# -----------------------------

def supervisor_node(state: GraphState):
    print("********************************** Superwiser Node Input ******************************")
    print(state)
    decision = supervisor.run(state)
    print("********************************** Superwiser Node Output ******************************")
    print(decision)

    context = ProcurementContext(
        item=decision.item,
        quantity=decision.quantity,
        budget=decision.budget,
        vendor=decision.vendor,
        specifications=decision.specifications,
        delivery_date=decision.delivery_date,
        current_stage=decision.current_stage,
    )

    return {
        "context": context,
        "next_agent": decision.next_agent,
        "workflow": decision.workflow,
        "supervisor_reasoning": decision.reasoning,
    }

def negotiator_node(state: GraphState):

    response = negotiator.run(state)

    return {
        "messages": [response]
    }


def financial_node(state: GraphState):

    response = financial.run(state)

    return {
        "messages": [response]
    }


def scraper_node(state: GraphState):

    response = scraper.run(state)

    return {
        "messages": [response]
    }


def rfq_node(state: GraphState):

    response = rfq.run(state)

    return {
        "messages": [response]
    }


# -----------------------------
# Build Graph
# -----------------------------

print("Building the graph")

builder = StateGraph(GraphState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("negotiator", negotiator_node)
builder.add_node("financial", financial_node)
builder.add_node("scraper", scraper_node)
builder.add_node("rfq", rfq_node)


builder.add_edge(START, "supervisor")


builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next_agent"],
    {
        "negotiator": "negotiator",
        "financial": "financial",
        "scraper": "scraper",
        "rfq": "rfq",
        "end": END,
    },
)


builder.add_edge("negotiator", END)
builder.add_edge("financial", END)
builder.add_edge("scraper", END)
builder.add_edge("rfq", END)


def get_graph(checkpointer):
    print("Compiling the graph")
    return builder.compile(checkpointer=checkpointer)