from dataclasses import dataclass


@dataclass
class IntentTestCase:
    query: str
    expected: str


TEST_CASES = [

    # -------------------------
    # General Chat
    # -------------------------

    IntentTestCase(
        "Who is the President of France?",
        "general_chat"
    ),

    IntentTestCase(
        "Explain Kubernetes.",
        "general_chat"
    ),

    IntentTestCase(
        "What is LangGraph?",
        "general_chat"
    ),

    IntentTestCase(
        "How does FastAPI work?",
        "general_chat"
    ),

    IntentTestCase(
        "Tell me a joke.",
        "general_chat"
    ),

    IntentTestCase(
        "Need help",
        "general_chat"
    ),

    IntentTestCase(
        "What is my name?",
        "general_chat"
    ),

    IntentTestCase(
        "Who manufactures Dell laptops?",
        "general_chat"
    ),

    IntentTestCase(
        "Thanks",
        "general_chat"
    ),

    IntentTestCase(
        "Forget everything",
        "general_chat"
    ),

    # -------------------------
    # Procurement
    # -------------------------

    IntentTestCase(
        "Need 100 Dell laptops",
        "procurement"
    ),

    IntentTestCase(
        "Buy 50 office chairs",
        "procurement"
    ),

    IntentTestCase(
        "Need 500 keyboards",
        "procurement"
    ),

    IntentTestCase(
        "Need 100 laptops under ₹50,000 each",
        "procurement"
    ),

    IntentTestCase(
        "Budget is ₹40 lakh",
        "procurement"
    ),

    IntentTestCase(
        "Delivery should be next Monday",
        "procurement"
    ),

    IntentTestCase(
        "Dell",
        "procurement"
    ),

    IntentTestCase(
        "Laptop",
        "procurement"
    ),

    IntentTestCase(
        "Use SSD only",
        "procurement"
    ),

    IntentTestCase(
        "Actually make it HP",
        "procurement"
    ),

    IntentTestCase(
        "Quotation",
        "procurement"
    ),

    IntentTestCase(
        "Generate an RFQ",
        "procurement"
    ),

    IntentTestCase(
        "Negotiate this quotation",
        "procurement"
    ),

    IntentTestCase(
        "Need help buying laptops",
        "procurement"
    ),

    IntentTestCase(
        "Compare Dell and HP suppliers",
        "procurement"
    ),
]