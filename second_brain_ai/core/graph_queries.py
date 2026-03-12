from typing import List, Dict, Any
from database.neo4j_client import get_neo4j_client
from core.schema_loader import get_schema_registry
from core.logging import get_logger


logger = get_logger(__name__)


class GraphQueryService:
    """
    High-level query utilities for the knowledge graph.
    """

    def __init__(self):

        self.client = get_neo4j_client()
        self.schema = get_schema_registry().get_graph_schema()

    def get_related_concepts(self, concept_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve concepts related to a given concept.
        """

        query = """
        MATCH (c:Concept {id:$id})-[:related_to]-(related:Concept)
        RETURN related
        """

        return self.client.run_query(query, {"id": concept_id})

    def get_domain_concepts(self, domain_name: str) -> List[Dict[str, Any]]:
        """
        Get all concepts belonging to a domain.
        """

        query = """
        MATCH (c:Concept)-[:belongs_to]->(d:Domain {name:$domain})
        RETURN c
        """

        return self.client.run_query(query, {"domain": domain_name})

    def get_dependencies(self, concept_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve prerequisite concepts.
        """

        query = """
        MATCH (c:Concept {id:$id})-[:depends_on]->(dep:Concept)
        RETURN dep
        """

        return self.client.run_query(query, {"id": concept_id})

    def find_concept_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Find concept nodes by name.
        """

        query = """
        MATCH (c:Concept {name:$name})
        RETURN c
        """

        return self.client.run_query(query, {"name": name})

    def get_node_relationships(self, node_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all relationships for a node.
        """

        query = """
        MATCH (n {id:$id})-[r]-(m)
        RETURN type(r) as relationship, m
        """

        return self.client.run_query(query, {"id": node_id})