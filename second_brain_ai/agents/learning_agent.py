import logging
from typing import Dict, Any

from second_brain_ai.agents.base_agent import BaseAgent
from second_brain_ai.services.gemini_service import GeminiService

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
            user_id = payload.get("user_id", "user_1")

            if not user_profile and user_id:
                from second_brain_ai.backend.database.neo4j_service import db
                user_node = db.get_node(user_id)
                if user_node:
                    known_concepts = [db.get_node(e["target"])["name"] for e in db.edges if e["source"] == user_id and e["type"] == "KNOWS"]
                    user_profile = {
                        "name": user_node.get("name"),
                        "known_concepts": known_concepts,
                        "instruction": "Tailor the learning module specifically matching what the user already knows."
                    }

            if not concept_data or not user_profile:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data and user_profile (or user_id) required"
                )

            request = {
                "concept": concept_data.get("name"),
                "known_concepts": user_profile.get("known_concepts", []),
                "user_profile": user_profile,
                "concept_data": concept_data
            }

            response = await self.ai_service.generate_learning_module(request)

            if "error" in response:
                return self.error_response("AGENT_FAILURE", response["error"])

            return self.success_response(response)

        except Exception as e:

            logger.exception("Learning agent execution failed")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )