import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class LearningAgent(BaseAgent):
    """
    Adapts research content to a user's learning style and profile.
    """

    def __init__(self, agent_name: str = "learning_agent"):
        super().__init__(agent_name)
        self.ai_service = GeminiService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expected payload:

        {
            "concept_data": {...},
            "user_profile": {...}
        }
        """

        try:

            concept_data = payload.get("concept_data")
            user_profile = payload.get("user_profile")

            if not concept_data or not user_profile:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data and user_profile required"
                )

            request = {
                "concept_data": concept_data,
                "user_profile": user_profile
            }

            response = await self.ai_service.generate_learning_module(request)

            return self.success_response(response)

        except Exception as e:

            logger.exception("Learning agent execution failed")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )