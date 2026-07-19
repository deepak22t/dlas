from langgraph.graph import StateGraph, START, END
from ai_core.agents.intent_classifier import IntentClassifier
from ai_core.agents.entity_extractor import EntityExtractor

from ai_core.agents.general_chat import GeneralChatAgent
from ai_core.nodes.state_manager import StateManager
from ai_core.nodes.requirement_validator import RequirementValidator
from ai_core.nodes.clarification import ClarificationAgent
from ai_core.nodes.planner import WorkflowPlanner
from ai_core.nodes.vendor_search import VendorSearchAgent
from ai_core.state import GraphState
from ai_core.nodes.rfq_agent import RFQGenerator,SendRFQAgent
from ai_core.nodes.quotation_collection import QuotationCollectionAgent
from ai_core.nodes.quotation_comparison import QuotationComparisonAgent
from ai_core.nodes.recommendation import RecommendationAgent
from app.core.logger import logger
from pprint import pprint

intent_classifier = IntentClassifier()
general_chat = GeneralChatAgent()
entity_extractor = EntityExtractor()
state_manager = StateManager()
comparison = QuotationComparisonAgent()
validator = RequirementValidator()
clarification = ClarificationAgent()
planner = WorkflowPlanner()
vendor_search_agent = VendorSearchAgent()
rfq_generator = RFQGenerator()
send_rfq_agent = SendRFQAgent()
quotation_collection = QuotationCollectionAgent()
recommendation = RecommendationAgent()

def intent_classifier_node(state):

    # print("=" * 60)
    # print("STATE RECEIVED BY INTENT")
    # pprint(state)
    # print("=" * 60)

    decision = intent_classifier.run(state)

    print("=" * 50)
    print("Intent Decision")
    pprint(decision)
    print("=" * 50)

    return {
    "intent": decision.intent,
    "confidence": decision.confidence,
    "reasoning": decision.reasoning,
   }


def general_chat_node(state):

    response = general_chat.run(state)

    return {

        "messages":[response]

    }

def route_after_intent(state: GraphState):
    if state["intent"] == "general_chat":
        return "general_chat"

    return "entity_extractor_node"

def entity_extractor_node(state: GraphState) -> GraphState:
    """    Placeholder for complete procurement workflow.

    Future:
    Intent
        ↓
    Entity Extraction
        ↓
    State Manager
        ↓
    Workflow Planner
        ↓
    Agent Orchestrator
    """
    entities = entity_extractor.run(state)

    print("="*50)
    print("Entity Extractor")
    pprint(entities)
    print("="*50)

    return {
        "entities": entities
    }

def state_manager_node(state):

    new_state = state_manager.run(state)

    print("=" * 50)
    print("STATE MANAGER")
    pprint(new_state)
    print("=" * 50)

    return new_state

def requirement_validator_node(state):

    result = validator.run(state)

    print("="*50)
    print("Requirement Validation")
    pprint(result)
    print("="*50)

    return {

        "validation": result

    }

def route_after_validation(state):

    if state["validation"].complete:
        return "planner"

    return "clarification"

def clarification_node(state):
    result = clarification.run(state)
    print("="*50)
    print("Clarification Agent")
    pprint(result)
    print("="*50)
    return result

def workflow_planner_node(state):
    result = planner.run(state)
    print("="*50)
    print(f"Workflow Planner")
    pprint(result)
    print("="*50)
    return result


def vendor_search_node(state):

    result = vendor_search_agent.run(state)

    print("=" * 50)
    print("Vendor Search")
    pprint(result)
    print("=" * 50)

    return result

def rfq_generator_node(state):

    result = rfq_generator.run(state)

    print("=" * 50)
    print("RFQ Generator")
    pprint(result)
    print("=" * 50)

    return result

def send_rfq_node(state: GraphState):

    result = send_rfq_agent.run(state)

    print("=" * 50)
    print("Send RFQ")
    pprint(result)
    print("=" * 50)

    return result

def quotation_collection_node(state:GraphState):
   result  = quotation_collection.run(state)
   print("=" * 50)
   print("Quatation Collection")
   pprint(result)
   print("=" * 50)

   return result

def quotation_comparison_node(state):
    result  = comparison.run(state)
    print("=" * 50)
    print("Quatation Comparison")
    pprint(result)
    print("=" * 50)

    return result

def recommendation_node(state):

    result = recommendation.run(state)

    print("=" * 50)

    print("Recommendation")

    print(result)

    print("=" * 50)

    return result

builder = StateGraph(GraphState)

builder.add_node("intent_classifier",intent_classifier_node)

builder.add_node("general_chat",general_chat_node)

builder.add_node("entity_extractor_node",entity_extractor_node)

builder.add_node("state_manager_node",state_manager_node)
builder.add_node("requirement_validator",requirement_validator_node)

builder.add_node("clarification",clarification_node)
builder.add_node("planner",workflow_planner_node)
builder.add_node("vendor_search",vendor_search_node)
builder.add_node("rfq_generator",rfq_generator_node)
builder.add_node("send_rfq",send_rfq_node)
builder.add_node("quotation_collection",quotation_collection_node)
builder.add_node("quotation_comparison",quotation_comparison_node)
builder.add_node("recommendation",recommendation_node,)

builder.add_edge(START, "intent_classifier")

builder.add_conditional_edges("intent_classifier",route_after_intent,
    {
        "general_chat": "general_chat",
        "entity_extractor_node": "entity_extractor_node",
    },
)

builder.add_edge("general_chat", END)
builder.add_edge("entity_extractor_node", "state_manager_node")
builder.add_edge(
    "state_manager_node",
    "requirement_validator",
)
builder.add_conditional_edges(
    "requirement_validator",
    route_after_validation,
    {
        "planner": "planner",
        "clarification": "clarification",
    },
)

builder.add_edge(
    "clarification",END
)
builder.add_edge(
    "planner","vendor_search"
)
builder.add_edge(
    "vendor_search","rfq_generator"
)
builder.add_edge(
    "rfq_generator",
    "send_rfq",
)
builder.add_edge(
    "send_rfq",
    "quotation_collection",
)
builder.add_edge(

    "quotation_collection",

    "quotation_comparison",

)
builder.add_edge(

    "quotation_comparison",

    "recommendation",

)

builder.add_edge(

    "recommendation",

    END,

)





def get_graph(checkpointer):
    return builder.compile(checkpointer=checkpointer)