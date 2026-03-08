from core.knowledge_graph import KnowledgeGraphService
from core.logging.logger import LoggerFactory


class GraphQueryUtilities:
    """
    Advanced query utilities for exploring the knowledge graph.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("graph_queries")
        self.graph = KnowledgeGraphService()

    def get_related_concepts(self, concept_id: str):
        """
        Fetch concepts related to a given concept.
        """
        query = """
        MATCH (c:Concept {id: $id})-[r]->(related)
        RETURN related
        """

        return self.graph.query(query, {"id": concept_id})

    def get_dependencies(self, concept_id: str):
        """
        Fetch concepts that a concept depends on.
        """
        query = """
        MATCH (c:Concept {id: $id})-[:depends_on]->(dep)
        RETURN dep
        """

        return self.graph.query(query, {"id": concept_id})

    def get_concepts_in_domain(self, domain_name: str):
        """
        Fetch all concepts belonging to a domain.
        """
        query = """
        MATCH (d:Domain {name: $name})<-[:belongs_to]-(c:Concept)
        RETURN c
        """

        return self.graph.query(query, {"name": domain_name})

    def find_shortest_path(self, concept_a: str, concept_b: str):
        """
        Find shortest conceptual connection path.
        """
        query = """
        MATCH (a:Concept {id: $a}),
              (b:Concept {id: $b}),
              p = shortestPath((a)-[*..5]-(b))
        RETURN p
        """

        return self.graph.query(query, {"a": concept_a, "b": concept_b})