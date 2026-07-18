from ai_core.llm_factory import LLMFactory
from app.core.logger import logger
from ai_core.agents.prompts import RFQ_PROMPT
from app.core.exceptions import AIServiceError

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


class RFQAgent:

    def __init__(self):
        self.llm = LLMFactory.create()

    def run(self, state):

        latest_user_message = None

        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                latest_user_message = msg
                break

        system_prompt = RFQ_PROMPT.format(
            context=state["context"]
        )

        payload = [
            SystemMessage(content=system_prompt),
            latest_user_message,
        ]

        try:
            return self.llm.invoke(payload)
        except Exception as exc:
            logger.exception("RFQAgent execution failed.")
            raise AIServiceError("RFQ agent failed.") from exc