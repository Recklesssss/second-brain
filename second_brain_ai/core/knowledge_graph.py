from typing import Dict, Any, List, Optional
from second_brain_ai.database.neo4j_client import get_neo4j_client
from second_brain_ai.core.schema_loader import get_schema_registry
from second_brain_ai.core.logging.logger import get_logger


logger = get_logger(__name__)


class KnowledgeGraphService:
    """
    Core CRUD operations for the knowledge graph.
    """

    def __init__(self):

        self.client = get_neo4j_client()
        self.schema = get_schema_registry().get_graph_schema()

        self.valid_labels = set(self.schema["node_labels"].keys())
        self.valid_relationships = set(self.schema["relationship_types"])

    def _validate_node_type(self, node_type: str):

        if node_type not in self.valid_labels:
            raise ValueError(f"Invalid node type: {node_type}")

    def _validate_relationship(self, rel_type: str):

        if rel_type not in self.valid_relationships:
            raise ValueError(f"Invalid relationship type: {rel_type}")

    def create_node(self, node_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:

        self._validate_node_type(node_type)

        query = f"""
        CREATE (n:{node_type} $props)
        RETURN n
        """

        result = self.client.run_query(query, {"props": properties})

        return result[0] if result else {}

    def get_node(self, node_type: str, node_id: str) -> Optional[Dict[str, Any]]:

        self._validate_node_type(node_type)

        query = f"""
        MATCH (n:{node_type} {{id: $id}})
        RETURN n
        """

        result = self.client.run_query(query, {"id": node_id})

        return result[0] if result else None

    def update_node(self, node_type: str, node_id: str, updates: Dict[str, Any]):

        self._validate_node_type(node_type)

        query = f"""
        MATCH (n:{node_type} {{id: $id}})
        SET n += $updates
        RETURN n
        """

        result = self.client.run_query(
            query,
            {"id": node_id, "updates": updates},
        )

        return result[0] if result else None

    def delete_node(self, node_type: str, node_id: str):

        self._validate_node_type(node_type)

        query = f"""
        MATCH (n:{node_type} {{id: $id}})
        DETACH DELETE n
        """

        self.client.run_query(query, {"id": node_id})

    def create_relationship(
        self,
        from_type: str,
        from_id: str,
        to_type: str,
        to_id: str,
        rel_type: str,
    ):

        self._validate_node_type(from_type)
        self._validate_node_type(to_type)
        self._validate_relationship(rel_type)

        query = f"""
        MATCH (a:{from_type} {{id:$from_id}})
        MATCH (b:{to_type} {{id:$to_id}})
        CREATE (a)-[r:{rel_type}]->(b)
        RETURN r
        """

        return self.client.run_query(
            query,
            {
                "from_id": from_id,
                "to_id": to_id,
            },
        )


_global_graph_service: Optional[KnowledgeGraphService] = None


def get_graph_service() -> KnowledgeGraphService:

    global _global_graph_service

    if _global_graph_service is None:
        _global_graph_service = KnowledgeGraphService()

    return _global_graph_service