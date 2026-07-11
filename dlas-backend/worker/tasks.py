from app.database.session import SessionLocal
from app.models.task import Task
from app.models.task import TaskStatus
from worker.celery_app import celery
from ai_core.graph import graph
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

        # Mark task as processing
        task.status = TaskStatus.PROCESSING
        db.commit()
        
        # Configuration metadata setup karein checkpointing ke liye
        thread_id = "test_id"
        config = {"configurable": {"thread_id": thread_id}}
        state = {
                    "task_id": task_id,
                    "messages": [HumanMessage(content=text)]
                }
        
        # Text input ko HumanMessage object me wrap karein
        response = graph.invoke(
            state,
            config=config,
        )
    
        # State ke aakhri message (Supervisor ka response) se content nikalein
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