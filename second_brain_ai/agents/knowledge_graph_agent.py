import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from services.graph_service import GraphService

logger = logging.getLogger(__name__)


class KnowledgeGraphAgent(BaseAgent):
    """
    Builds knowledge graph nodes and relationships
    from concept research data.
    """

    def __init__(self, agent_name: str = "knowledge_graph_agent"):
        super().__init__(agent_name)
        self.graph_service = GraphService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        try:

            concept_data = payload.get("concept_data")

            if not concept_data:
                return self.error_response(
                    "AGENT_FAILURE",
                    "concept_data required"
                )

            concept = concept_data.get("concept")
            relations = concept_data.get("relations", [])

            node_id = await self.graph_service.create_concept_node(concept)

            for relation in relations:

                await self.graph_service.create_relationship(
                    node_id,
                    relation["target"],
                    relation["type"]
                )

            return self.success_response({
                "node_id": node_id,
                "relations_created": len(relations)
            })

        except Exception as e:

            logger.exception("Knowledge graph build failed")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )