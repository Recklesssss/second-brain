from neo4j import GraphDatabase
import os
import logging


class Neo4jClient:
    """
    Central Neo4j connection manager for the AI Second Brain.
    """

    def __init__(
        self,
        uri: str = None,
        username: str = None,
        password: str = None
    ):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")

        self.driver = None

    def connect(self):
        """
        Initialize Neo4j connection.
        """
        if self.driver is None:
            logging.info("Connecting to Neo4j")
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )

    def close(self):
        """
        Close Neo4j connection.
        """
        if self.driver:
            logging.info("Closing Neo4j connection")
            self.driver.close()
            self.driver = None

    def run_query(self, query: str, parameters: dict = None):
        """
        Execute a Cypher query.
        """
        if self.driver is None:
            raise RuntimeError("Neo4j client is not connected")

        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def test_connection(self):
        """
        Verify the connection to Neo4j.
        """
        result = self.run_query("RETURN 1 AS test")
        return result[0]["test"] == 1