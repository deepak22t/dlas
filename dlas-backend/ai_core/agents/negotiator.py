from ai_core.llm_factory import LLMFactory
from app.core.logger import logger
from ai_core.agents.prompts import NEGOTIATOR_PROMPT
from app.core.exceptions import AIServiceError

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


class NegotiatorAgent:

    def __init__(self):
        self.llm = LLMFactory.create()

    def run(self, state):

        latest_user_message = None

        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                latest_user_message = msg
                break

        system_prompt = NEGOTIATOR_PROMPT.format(
            context=state["context"]
        )

        payload = [
            SystemMessage(content=system_prompt),
            latest_user_message,
        ]

        try:
            return self.llm.invoke(payload)
        except Exception as exc:
            logger.exception("NegotiatorAgent execution failed.")
            raise AIServiceError("Negotiator agent failed.") from exc