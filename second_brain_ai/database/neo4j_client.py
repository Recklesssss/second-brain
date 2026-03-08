from neo4j import GraphDatabase
from config.environment import EnvironmentConfig
from core.logging.logger import LoggerFactory, ErrorLogger


class Neo4jClient:
    """
    Neo4j database connection manager
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("neo4j_client")

        self.uri = EnvironmentConfig.require("NEO4J_URI")
        self.user = EnvironmentConfig.require("NEO4J_USER")
        self.password = EnvironmentConfig.require("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )

    def close(self):
        if self.driver:
            self.driver.close()

    def test_connection(self):
        """
        Verify database connectivity
        """
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                return result.single()["test"] == 1
        except Exception as e:
            ErrorLogger.log_error("neo4j_client", str(e))
            return False

    def execute_query(self, query: str, parameters: dict = None):
        """
        Execute Cypher query
        """
        parameters = parameters or {}

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]

        except Exception as e:
            ErrorLogger.log_error("neo4j_client", str(e))
            raise