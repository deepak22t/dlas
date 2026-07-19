from langchain.chat_models import init_chat_model
from app.core.config import get_settings

settings = get_settings()


class LLMFactory:
    @staticmethod
    def create():
        # return ChatGroq(
        #     model=settings.groq_model,
        #     api_key=settings.groq_api_key,
        #     temperature=0,
        # )
        
        return init_chat_model(
            "auto",
            model_provider="openrouter",
            api_key=settings.open_api_key,
            temperature=0,
            # OpenRouter reserves credits from max_tokens; "auto" defaults to 65536.
            max_tokens=1024,
        )