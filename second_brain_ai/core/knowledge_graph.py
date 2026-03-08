from database.neo4j_client import Neo4jClient
from core.schema_loader import SchemaRegistryLoader
from core.logging.logger import LoggerFactory


class KnowledgeGraphService:
    """
    CRUD service for interacting with the Neo4j knowledge graph.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("knowledge_graph")
        self.db = Neo4jClient()
        self.schema = SchemaRegistryLoader()

        self.node_labels = self.schema.get_node_labels()
        self.relationship_types = self.schema.get_relationship_types()

    def create_node(self, label: str, properties: dict):
        if label not in self.node_labels:
            raise ValueError(f"Invalid node label: {label}")

        query = f"""
        CREATE (n:{label} $props)
        RETURN n
        """

        result = self.db.execute_query(query, {"props": properties})
        return result

    def get_node_by_id(self, label: str, node_id: str):
        query = f"""
        MATCH (n:{label} {{id: $id}})
        RETURN n
        """

        result = self.db.execute_query(query, {"id": node_id})
        return result

    def create_relationship(
        self,
        from_label: str,
        from_id: str,
        to_label: str,
        to_id: str,
        relationship: str
    ):

        if relationship not in self.relationship_types:
            raise ValueError(f"Invalid relationship type: {relationship}")

        query = f"""
        MATCH (a:{from_label} {{id: $from_id}})
        MATCH (b:{to_label} {{id: $to_id}})
        CREATE (a)-[r:{relationship}]->(b)
        RETURN r
        """

        return self.db.execute_query(
            query,
            {
                "from_id": from_id,
                "to_id": to_id
            }
        )

    def query(self, cypher_query: str, parameters: dict = None):
        return self.db.execute_query(cypher_query, parameters or {})