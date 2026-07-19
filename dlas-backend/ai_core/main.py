
from langchain_core.messages import HumanMessage

from ai_core.graph import get_graph
from ai_core.state import get_postgres_checkpointer
from uuid import uuid4
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

print("Starting the workflow")


def get_initial_state(message):
    return {
        "task_id": "task-1",
        "messages": [HumanMessage(content=message)],
    }


thread_id = str(uuid4())

def get_response(workflow, initial_state):
    response = workflow.invoke(
        initial_state,
        config={"configurable": {"thread_id": thread_id }},
    )
    # Specialist agents append AI messages; supervisor-only (end) does not.
    return response["messages"][-1].content


def run_workflow(message):
    with get_postgres_checkpointer() as checkpointer:
        checkpointer.setup()  #setup the checkpointer ye sirf ek baar hi call karna hai future improvements mein
        workflow = get_graph(checkpointer)
        #print(workflow.get_graph().draw_mermaid())
        initial_state=get_initial_state(message)
        response = get_response(workflow,initial_state)
        print("AI:")
        print(response)

while True:
    print("You: ")
    message = input()
    if message == 'exit':
        break
    else:
        run_workflow(message)