from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from ai_core.prompts import SYSTEM_PROMPT
from app.core.config import get_settings
from app.core.logger import logger
from app.core.exceptions import AIServiceError
from ai_core.llm_factory import get_llm

settings = get_settings()

class AIService:
    """
    Service responsible for communicating with the LLM.
    """

    def __init__(self) -> None:
       self.llm = get_llm()

    def generate_response(self, prompt: str) -> str:
        """
        Generate an AI response for the given prompt.
        """

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        try:
            logger.info("Sending request to Groq LLM.")

            # response = self.llm.invoke(messages)

            logger.info("LLM response generated successfully.")

            # return response.content
            return "Mock response"
        
        except Exception as exc:
            logger.exception("Failed to generate response from LLM.")   

            raise AIServiceError(
                "Unable to generate AI response."
            ) from exc