from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
)

from ai_core.agents.prompts import INTENT_PROMPT
from ai_core.llm_factory import LLMFactory
from ai_core.state import IntentDecision,GraphState
from app.core.exceptions import AIServiceError
from app.core.logger import logger


class IntentClassifier:

    def __init__(self):

        self.llm = (
            LLMFactory
            .create()
            .with_structured_output(IntentDecision)
        )

    def run(self, state: GraphState)-> IntentDecision:

        latest_message = state["messages"][-1]

        full_payload = [

            SystemMessage(
                content=INTENT_PROMPT
            ),

            latest_message,

        ]

        try:
            
            
            return self.llm.invoke(full_payload)

        except Exception as exc:

            logger.exception(
                "Intent classification failed."
            )

            raise AIServiceError(
                "Intent classification failed."
            ) from exc