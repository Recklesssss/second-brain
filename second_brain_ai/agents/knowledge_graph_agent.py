import logging
from typing import Dict, Any

from second_brain_ai.agents.base_agent import BaseAgent
from second_brain_ai.core.knowledge_graph import KnowledgeGraphService

logger = logging.getLogger(__name__)


class KnowledgeGraphAgent(BaseAgent):
    """
    Builds knowledge graph nodes and relationships
    from concept research data.
    """

    def __init__(self, agent_name: str = "knowledge_graph_agent"):
        super().__init__(agent_name)
        self.graph_service = KnowledgeGraphService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        try:

            concept_data = payload.get("concept_data")

            if not concept_data:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data required"
                )

            concept_name = concept_data.get("concept")
            relations = concept_data.get("relations", [])

            # Create concept node
            node = self.graph_service.create_node("Concept", {"name": concept_name, "id": concept_name})
            node_id = node.get("id", concept_name)

            relations_created = 0
            for relation in relations:
                try:
                    self.graph_service.create_relationship(
                        "Concept", node_id,
                        "Concept", relation["target"],
                        relation["type"]
                    )
                    relations_created += 1
                except Exception as e:
                    logger.warning(f"Failed to create relationship: {e}")

            return self.success_response({
                "node_id": node_id,
                "relations_created": relations_created
            })

        except Exception as e:

            logger.exception("Knowledge graph build failed")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )