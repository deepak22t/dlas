from fastapi import FastAPI
from pydantic import BaseModel
from graph import app_graph
app = FastAPI()

class ChatRequest(BaseModel):
 text: str

@app.post("/api/chat")
def handle_chat(request: ChatRequest):
    print(f"User ne bheja: {request.text}")
    initial_state = {"messages": [request.text]}
    config = {"configurable": {"thread_id": "test_user_1"}}
    result = app_graph.invoke(initial_state, config=config)
    final_message = result["messages"][-1]
    return {"status": "success", "agent_reply": final_message}

@app.post("/api/webhook")
def handle_webhook():
    return {"status": "success"}
   
  