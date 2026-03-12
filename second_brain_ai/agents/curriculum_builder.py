import logging
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from core.knowledge_graph import KnowledgeGraphClient

logger = logging.getLogger(__name__)


class CurriculumBuilderAgent(BaseAgent):
    """
    Generates a structured curriculum for a given domain.
    """

    def __init__(self, agent_name: str = "curriculum_builder_agent"):
        super().__init__(agent_name)
        self.kg_client = KnowledgeGraphClient()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            domain: str = payload.get("domain")
            if not domain:
                return self.error_response(
                    "AGENT_FAILURE", "Payload must include 'domain'"
                )

            # Retrieve concepts for domain
            concepts = self.kg_client.get_concepts(domain)
            learning_sequence = [c["name"] for c in concepts]

            # Build prerequisite graph
            prerequisite_graph = {
                c["name"]: [dep["name"] for dep in c.get("prerequisites", [])]
                for c in concepts
            }

            return self.success_response({
                "domain": domain,
                "learning_sequence": learning_sequence,
                "prerequisite_graph": prerequisite_graph
            })

        except Exception as e:
            logger.exception("Curriculum generation failed")
            return self.error_response("AGENT_FAILURE", str(e))