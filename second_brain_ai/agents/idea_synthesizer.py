import logging
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class IdeaSynthesizerAgent(BaseAgent):
    """
    Combines multiple concepts to generate a new idea.
    """

    def __init__(self, agent_name: str = "idea_synthesizer_agent"):
        super().__init__(agent_name)
        self.ai_service = GeminiService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            concepts: List[Dict[str, Any]] = payload.get("concepts")

            if not concepts or not isinstance(concepts, list):
                return self.error_response(
                    "AGENT_FAILURE",
                    "Payload must include a list of concepts"
                )

            # Use Gemini service to generate idea
            idea_result = await self.ai_service.generate_idea(concepts)

            return self.success_response({
                "idea_title": idea_result.get("title"),
                "description": idea_result.get("description"),
                "related_concepts": idea_result.get("related_concepts", []),
                "potential_applications": idea_result.get("potential_applications", [])
            })

        except Exception as e:
            logger.exception("Idea generation failed")
            return self.error_response("AGENT_FAILURE", str(e))