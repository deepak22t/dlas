# Future Improvements

## Phase 4

### Milestone 4.4

Current Implementation
- Graph is compiled for every request.
- Checkpointer is created using a context manager.

Future Improvement
- Create a singleton PostgresSaver.
- Compile the graph only once during application startup.
- Reuse the compiled graph across all worker requests.

Priority: Medium
Reason:
Current implementation is correct and suitable for learning. Optimize after conversation recovery is implemented.

## Phase 5

- Add conditional routing.
- Replace single supervisor with multi-agent routing.
- Parallel execution.

## Phase 9

- Replace print with logger.
- Metrics.
- Tracing.
- Unit tests.
- Integration tests.
- Docker optimization.




Future Improvements

□ Repository Pattern

□ Unit Testing

□ Integration Testing

□ JWT Refresh Tokens

□ Rate Limiting

□ Structured Logging

□ OpenTelemetry

□ Prometheus

□ Grafana

□ Docker Compose Profiles

□ Kubernetes

□ Multi-tenant Architecture

□ Vendor Ranking ML Model

□ LLM Cost Tracking

□ AI Evaluation Pipeline

□ Retry Policies

□ Dead Letter Queue

□ Caching Strategy

□ Streaming Responses

□ WebSocket Updates

□ Event Driven Architecture











****************************Improvement:1****************************

 checkpointer.setup()  #setup the checkpointer ye sirf ek baar hi call karna hai future improvements mein



# startup
checkpointer.setup()

# runtime
with get_postgres_checkpointer() as checkpointer:
    workflow = get_graph(checkpointer)
    workflow.invoke(...)


************************Imrovement:2**********************************
class ProcurementContext(BaseModel):
    requirement: str = ""          # e.g., "Dell Laptop", "Office Chairs", "Cisco Switches"
    quantity: int | None = None
    budget: float | None = None
    preferred_vendor: str = ""
    specifications: str = ""
    delivery_location: str = ""
    delivery_date: str = ""
    currency: str = "INR"
    current_stage: str = "requirement_collection"   




    ProcurementContext ko aisa banao


    
************************Imrovement:3**********************************

 super decsision me nested output schema implementation for context