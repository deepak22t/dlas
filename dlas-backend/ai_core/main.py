
from langchain_core.messages import HumanMessage

from ai_core.graph import get_graph
from ai_core.state import get_postgres_checkpointer
from uuid import uuid4
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

print("Starting the workflow")


def get_initial_state(message,task_id):
    return {
        "task_id":  task_id,
        "messages": [HumanMessage(content=message)],
    }


thread_id = str(uuid4())

def get_response(workflow, initial_state,task_id):
    final_state = workflow.invoke(
        initial_state,
        config={"configurable": {"thread_id": task_id }},
    )
    # Specialist agents append AI messages; supervisor-only (end) does not.
    #return final_state["messages"][-1].content
    return final_state


def run_workflow(message,task_id):
    with get_postgres_checkpointer() as checkpointer:
        checkpointer.setup()  #setup the checkpointer ye sirf ek baar hi call karna hai future improvements mein
        workflow = get_graph(checkpointer)
        #print(workflow.get_graph().draw_mermaid())
        initial_state=get_initial_state(message,task_id)
        response = get_response(workflow,initial_state,task_id)
        print("AI:")
        print(response)
        return response



def process_task_without_celery(task_id, user_request):
   return run_workflow(user_request,task_id)



# while True:
#     print("You: ")
#     message = input()
#     if message == 'exit':
#         break
#     else:
#         run_workflow(message)