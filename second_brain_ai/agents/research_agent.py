import logging
from typing import Dict, Any

from second_brain_ai.agents.base_agent import BaseAgent
from second_brain_ai.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """
    Agent responsible for researching concepts.

    Uses Gemini service to produce structured research data
    based on prompts defined in PROMPT_LIBRARY.yaml.
    """

    def __init__(self, agent_name: str = "research_agent"):
        super().__init__(agent_name)
        self.ai_service = GeminiService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expected payload:

        {
            "concept": "Graph Neural Networks",
            "domain": "Machine Learning"
        }
        """

        try:

            concept = payload.get("concept")
            domain = payload.get("domain")

            if not concept or not domain:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept and domain required"
                )

            prompt_data = {
                "concept": concept,
                "domain": domain
            }

            response = await self.ai_service.generate_research(prompt_data)

            if "error" in response:
                return self.error_response("AGENT_FAILURE", response["error"])

            return self.success_response(response)

        except Exception as e:

            logger.exception("Research agent failure")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )