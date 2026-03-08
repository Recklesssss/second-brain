import os
from database.neo4j_client import Neo4jClient


def setup_module():
    os.environ["NEO4J_URI"] = "bolt://localhost:7687"
    os.environ["NEO4J_USER"] = "neo4j"
    os.environ["NEO4J_PASSWORD"] = "password"


def test_client_initialization():
    client = Neo4jClient()
    assert client.uri is not None
    client.close()


def test_connection_method_exists():
    client = Neo4jClient()
    assert hasattr(client, "test_connection")
    client.close()


def test_query_execution_interface():
    client = Neo4jClient()
    assert hasattr(client, "execute_query")
    client.close()