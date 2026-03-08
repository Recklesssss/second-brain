import yaml
from pathlib import Path

from database.neo4j_client import Neo4jClient


class GraphSchemaInitializer:
    """
    Initializes the Neo4j graph schema according to
    the global schema registry.
    """

    def __init__(self, schema_path="config/schema_registry.yaml"):

        self.schema_path = Path(schema_path)

        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema registry not found: {schema_path}")

        with open(self.schema_path) as f:
            self.schema = yaml.safe_load(f)

        self.client = Neo4jClient()

    def initialize(self):

        self.client.connect()

        graph_schema = self.schema["schema_registry"]["graph_schema"]

        self._create_node_constraints(graph_schema)
        self._register_relationship_types(graph_schema)

    def _create_node_constraints(self, graph_schema):

        node_labels = graph_schema["node_labels"]

        for label in node_labels:

            query = f"""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (n:{label})
            REQUIRE n.id IS UNIQUE
            """

            self.client.run_query(query)

    def _register_relationship_types(self, graph_schema):

        relationships = graph_schema["relationship_types"]

        for rel in relationships:

            # Neo4j does not require explicit creation of relationship types,
            # but we register them by creating metadata nodes.

            query = """
            MERGE (r:RelationshipType {name: $name})
            """

            self.client.run_query(query, {"name": rel})

    def verify_schema(self):

        result = self.client.run_query(
            "MATCH (r:RelationshipType) RETURN r.name AS name"
        )

        return [r["name"] for r in result]

    def close(self):

        self.client.close()