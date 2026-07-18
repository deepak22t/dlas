from langchain_core.messages import SystemMessage

from ai_core.agents.prompts import SYSTEM_PROMPT
from ai_core.llm_factory import LLMFactory
from ai_core.state import SupervisorDecision
from app.core.exceptions import AIServiceError
from app.core.logger import logger


class SupervisorAgent:
    def __init__(self) -> None:
        # Groq llama-3.1-* often fails function_calling (`tool_use_failed`).
        # json_mode matches our prompt ("Return ONLY valid JSON").
        self.llm = LLMFactory.create().with_structured_output(
            SupervisorDecision,
            method="json_mode",
        )

    def run(self, state) -> SupervisorDecision:
        """
        Analyze conversation + procurement context and decide
        which specialist agent should run next.
        """
        context = state["context"]
        system = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Current procurement context:\n{context.model_dump_json()}\n"
            f"Current workflow: {state.get('workflow', '')}"
        )

        full_payload = [
            SystemMessage(content=system),
            *state["messages"],
        ]

        try:
            return self.llm.invoke(full_payload)

        except Exception as exc:
            logger.exception("SupervisorAgent execution failed.")
            raise AIServiceError("Supervisor agent failed.") from exc
