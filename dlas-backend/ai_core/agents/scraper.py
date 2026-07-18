from ai_core.llm_factory import LLMFactory
from app.core.logger import logger
from ai_core.agents.prompts import SCRAPER_PROMPT
from app.core.exceptions import AIServiceError

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


class ScraperAgent:

    def __init__(self):
        self.llm = LLMFactory.create()

    def run(self, state):

        latest_user_message = None

        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                latest_user_message = msg
                break

        system_prompt = SCRAPER_PROMPT.format(
            context=state["context"]
        )

        payload = [
            SystemMessage(content=system_prompt),
            latest_user_message,
        ]

        try:
            return self.llm.invoke(payload)
        except Exception as exc:
            logger.exception("ScraperAgent execution failed.")
            raise AIServiceError("Scraper agent failed.") from exc