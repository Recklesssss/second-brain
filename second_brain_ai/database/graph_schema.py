from typing import List
from second_brain_ai.database.neo4j_client import get_neo4j_client
from second_brain_ai.core.schema_loader import get_schema_registry
from second_brain_ai.core.logging.logger import get_logger


logger = get_logger(__name__)


class GraphSchemaInitializer:
    """
    Initializes Neo4j schema constraints based on SCHEMA_REGISTRY.
    """

    def __init__(self):
        self.client = get_neo4j_client()
        self.schema = get_schema_registry().get_graph_schema()

    def _create_constraint(self, query: str):

        try:
            self.client.run_query(query)
        except Exception as e:
            logger.warning(
                f"Constraint creation failed or already exists: {query}",
                extra={"event": "schema_constraint"},
            )

    def initialize_constraints(self):

        node_labels = self.schema.get("node_labels", {})

        for label, config in node_labels.items():

            if "id" in config.get("required_fields", []):

                constraint_query = f"""
                CREATE CONSTRAINT IF NOT EXISTS
                FOR (n:{label})
                REQUIRE n.id IS UNIQUE
                """

                self._create_constraint(constraint_query)

    def initialize_indexes(self):

        node_labels = self.schema.get("node_labels", {})

        for label in node_labels.keys():

            index_query = f"""
            CREATE INDEX IF NOT EXISTS
            FOR (n:{label})
            ON (n.name)
            """

            try:
                self.client.run_query(index_query)
            except Exception:
                logger.warning(
                    f"Index creation failed or exists for label {label}",
                    extra={"event": "schema_index"},
                )

    def initialize(self):

        logger.info(
            "Initializing graph schema",
            extra={"event": "schema_initialization"},
        )

        self.initialize_constraints()
        self.initialize_indexes()


def initialize_graph_schema():

    initializer = GraphSchemaInitializer()
    initializer.initialize()