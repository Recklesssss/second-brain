from database.neo4j_client import Neo4jClient
from core.schema_loader import SchemaRegistryLoader
from core.logging.logger import LoggerFactory


class GraphSchemaInitializer:
    """
    Initializes and validates Neo4j schema
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("graph_schema")
        self.db = Neo4jClient()
        self.schema = SchemaRegistryLoader()

    def initialize_constraints(self):
        """
        Create unique constraints for node IDs
        """
        node_labels = self.schema.get_node_labels()

        for label in node_labels.keys():
            query = f"""
            CREATE CONSTRAINT IF NOT EXISTS
            FOR (n:{label})
            REQUIRE n.id IS UNIQUE
            """
            self.db.execute_query(query)

            self.logger.info(f"Constraint created for {label}.id")

    def prevent_duplicate_concepts(self):
        """
        Prevent duplicate Concept nodes by name
        """
        query = """
        CREATE CONSTRAINT IF NOT EXISTS
        FOR (c:Concept)
        REQUIRE c.name IS UNIQUE
        """
        self.db.execute_query(query)

    def validate_relationship_type(self, relationship: str):
        """
        Ensure relationship type exists in schema
        """
        allowed = self.schema.get_relationship_types()

        if relationship not in allowed:
            raise ValueError(f"Invalid relationship type: {relationship}")

    def initialize(self):
        """
        Run all schema initialization steps
        """
        self.initialize_constraints()
        self.prevent_duplicate_concepts()