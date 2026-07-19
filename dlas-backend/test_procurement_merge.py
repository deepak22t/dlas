from langchain_core.messages import HumanMessage

from ai_core.graph import get_graph
from ai_core.state import get_postgres_checkpointer

THREAD_ID = "test-procurement-merge"


def run_turn(workflow, message: str):
    state = {
        "task_id": "task-1",
        "messages": [HumanMessage(content=message)],
    }
    return workflow.invoke(
        state,
        config={"configurable": {"thread_id": THREAD_ID}},
    )


def main():
    with get_postgres_checkpointer() as checkpointer:
        checkpointer.setup()
        workflow = get_graph(checkpointer)

        run_turn(workflow, "i want to buy 10 PC's")
        r2 = run_turn(workflow, "actually 20 PC's")
        r3 = run_turn(workflow, "no 30")

        print("Turn 2 procurement:", r2.get("procurement"))
        print("Turn 3 procurement:", r3.get("procurement"))


if __name__ == "__main__":
    main()
