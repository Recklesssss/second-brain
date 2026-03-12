import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class QuestionGenerator(BaseAgent):
    """
    Generates learning questions for a given concept.
    """

    def __init__(self, agent_name: str = "question_generator"):
        super().__init__(agent_name)
        self.ai_service = GeminiService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expected payload:

        {
            "concept_data": {...}
        }
        """

        try:

            concept_data = payload.get("concept_data")

            if not concept_data:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data required"
                )

            response = await self.ai_service.generate_questions(concept_data)

            return self.success_response(response)

        except Exception as e:

            logger.exception("Question generator failure")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )