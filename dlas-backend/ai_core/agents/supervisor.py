from langchain_core.messages import (
    AnyMessage,
    AIMessage,
    SystemMessage,
)

from ai_core.agents.prompts import SYSTEM_PROMPT
from ai_core.llm_factory import LLMFactory
from app.core.exceptions import AIServiceError
from app.core.logger import logger


class SupervisorAgent:
    def __init__(self) -> None:
        self.llm = LLMFactory.create()

    def run(self, messages: list[AnyMessage]) -> AIMessage:
        """
        Accept the conversation history, prepend the system prompt,
        and generate the next assistant response.
        """

        full_payload = [SystemMessage(content=SYSTEM_PROMPT)] + messages

        try:
            return self.llm.invoke(full_payload)

        except Exception as exc:
            logger.exception("SupervisorAgent execution failed.")
            raise AIServiceError("Supervisor agent failed.") from exc