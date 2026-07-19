from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    AIMessage,
)

from ai_core.agents.prompts import GENERAL_CHAT_PROMPT
from ai_core.state import GraphState
from ai_core.llm_factory import LLMFactory
from app.core.exceptions import AIServiceError
from app.core.logger import logger


class GeneralChatAgent:

    def __init__(self):
        self.llm = LLMFactory.create()

    def run(self, state: GraphState)-> AIMessage:

        latest_message = state["messages"][-1]

        payload = [
            SystemMessage(content=GENERAL_CHAT_PROMPT),
            latest_message,
        ]

        try:
            return self.llm.invoke(payload)

        except Exception as exc:
            logger.exception("GeneralChatAgent execution failed.")
            raise AIServiceError(
                "GeneralChatAgent failed."
            ) from exc