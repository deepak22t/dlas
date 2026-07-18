DLAS is an AI-powered Multi-Agent Procurement Assistant.

Instead of acting as a chatbot, it automates the complete procurement workflow.

The system is designed to:

• Understand procurement requirements
• Discover vendors
• Send RFQs
• Negotiate quotations
• Compare financial offers
• Recommend the best vendor
• Maintain complete procurement history

The long-term goal is to build a production-grade AI procurement platform capable of autonomous vendor communication and decision support.


React Native

↓

FastAPI Gateway

↓

Redis

↓

Celery

↓

LangGraph

↓

MCP

↓

WhatsApp

↓

Vendor



















                                    CURRENT IMPLEMENTED ARCHITECTURE
                                   (End of Phase 4 - Milestone 4.4)

                                        ┌───────────────────────┐
                                        │       Client          │
                                        │  (Postman / Future RN)│
                                        └───────────┬───────────┘
                                                    │
                                              HTTP Request
                                                    │
                                                    ▼
                                ┌──────────────────────────────────┐
                                │          FastAPI App             │
                                │            app/main.py           │
                                └───────────────┬──────────────────┘
                                                │
                           Startup (lifespan)   │
                                                │
            ┌───────────────────────────────────┼────────────────────────────────┐
            │                                   │                                │
            ▼                                   ▼                                ▼
  check_database_connection()        PostgresSaver.setup()             API Routers Registered
            │                                   │
            │                                   │
            ▼                                   ▼
      PostgreSQL OK                 LangGraph checkpoint tables
            │
            ▼
────────────────────────────────────────────────────────────────────────────────────────────

                    POST /chat
                         │
                         ▼
                app/api/chat.py
                         │
                         ▼
              chat_service.py
                         │
                         ▼
          Create Task in PostgreSQL
                         │
                         ▼
          celery.delay(task_id,text)
                         │
─────────────────────────┼──────────────────────────────────────────────────────────────────

                    Redis Broker
                         │
                         ▼
               Celery Worker
           worker/tasks.py
                         │
                         ▼
          Load Task from Database
                         │
                         ▼
        status = PROCESSING
                         │
                         ▼
        Build Graph State

        {
          task_id,
          messages=[HumanMessage]
        }

                         │
                         ▼
       config = {
          thread_id
       }

                         │
                         ▼
      get_postgres_checkpointer()
                         │
                         ▼
      get_graph(checkpointer)
                         │
                         ▼
      graph.invoke(state, config)
                         │
─────────────────────────┼──────────────────────────────────────────────────────────────────

                     LangGraph

                  START
                    │
                    ▼
            Supervisor Node
                    │
                    ▼
           SupervisorAgent
                    │
                    ▼
             ChatGroq LLM
                    │
                    ▼
             AI Response
                    │
                    ▼
                  END

          ▲
          │
          │
   PostgresSaver
          │
          ▼
Checkpoint Database
(messages, thread state,
graph state)

─────────────────────────┼──────────────────────────────────────────────────────────────────

               Worker Receives Response
                         │
                         ▼
      Task.status = COMPLETED
      Task.result = response
                         │
                         ▼
            Commit PostgreSQL
                         │
                         ▼
         GET /history can read results









                         User
                  │
                  ▼
        Supervisor (Brain)
        -------------------
        ✓ Understand intent
        ✓ Maintain workflow
        ✓ Track active agent
        ✓ Maintain task context
        ✓ Prepare agent input
        ✓ Route to correct agent
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 Negotiator           Financial
        ▼                   ▼
        └─────────┬─────────┘
                  ▼
          Response to User