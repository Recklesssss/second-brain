import logging
from typing import Dict, Any

from second_brain_ai.agents.base_agent import BaseAgent
from second_brain_ai.services.gemini_service import GeminiService

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
            user_id = payload.get("user_id", "user_1")

            if not concept_data:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data required"
                )

            if user_id and "name" in concept_data:
                from second_brain_ai.backend.database.neo4j_service import db
                # Find matching concept node by name to get its ID safely
                concepts = [n for n in db.get_nodes_by_label("Concept") if n["name"] == concept_data["name"]]
                if concepts:
                    concept_id = concepts[0]["id"]
                    # Calculate mastery
                    masteries = [e.get("properties", {}).get("mastery_level", 0) for e in db.edges if e["source"] == user_id and e["target"] == concept_id and e["type"] == "KNOWS"]
                    if masteries:
                        concept_data["user_mastery_level"] = max(masteries)
                        concept_data["instruction"] = f"Generate questions matching mastery level {max(masteries)}/1.0."

            response = await self.ai_service.generate_questions(concept_data)

            if "error" in response:
                return self.error_response("AGENT_FAILURE", response["error"])

            return self.success_response(response)

        except Exception as e:

            logger.exception("Question generator failure")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )