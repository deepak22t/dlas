from langchain_groq import ChatGroq

from app.core.config import get_settings

settings = get_settings()


class LLMFactory:
    @staticmethod
    def create():
        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0,
        )