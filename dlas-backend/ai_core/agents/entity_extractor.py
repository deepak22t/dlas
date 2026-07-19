from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
)

from ai_core.agents.prompts import ENTITY_EXTRACTION_PROMPT
from ai_core.llm_factory import LLMFactory
from ai_core.state import ProcurementEntities,GraphState
from app.core.exceptions import AIServiceError
from app.core.logger import logger


class EntityExtractor:

    def __init__(self):

        self.llm = (
            LLMFactory
            .create()
            .with_structured_output(ProcurementEntities)
        )

    def run(self, state: GraphState)-> ProcurementEntities:

        latest_message = state["messages"][-1]

        full_payload = [

            SystemMessage(
                content=ENTITY_EXTRACTION_PROMPT
            ),

            latest_message,

        ]

        try:

            return self.llm.invoke(full_payload)

        except Exception as exc:

            logger.exception(
                "Entity Extraction failed."
            )

            raise AIServiceError(
                "Entity Extraction failed."
            ) from exc