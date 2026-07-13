from app.database.session import SessionLocal
from app.models.task import Task
from app.models.task import TaskStatus
from worker.celery_app import celery
from ai_core.graph import get_graph
from ai_core.state import get_postgres_checkpointer
# Ye import missing tha:
from langchain_core.messages import HumanMessage

@celery.task(name="process_chat_task")
def process_chat_task(task_id: str, text: str) -> str:
    """
    Process a chat request in the background.
    """

    db = SessionLocal()

    try:
        task = db.get(Task, task_id)

        if task is None:
            return "Task not found"

        task.status = TaskStatus.PROCESSING
        db.commit()
        

        #lang Graph playing here
        thread_id = str(task_id)                                      # to find check pointer need thread id (super set)
        config = {"configurable": {"thread_id": thread_id}}       #configration basically is thread id k bases pe hue converastaion ko lega as a memory context

        state = {                                                 #   inital_state defining here
                    "task_id": task_id,
                    "messages": [HumanMessage(content=text)]
                }
        
        with get_postgres_checkpointer() as checkpointer:
            graph = get_graph(checkpointer)
            response = graph.invoke(
                state,
                config=config,
            )
            result = response["messages"][-1].content
    


        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()

        return result

    except Exception as exc:
        db.rollback()

        if task is not None:
            task.status = TaskStatus.FAILED
            db.commit()

        raise

    finally:
        db.close()