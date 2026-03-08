import pytest
from database.neo4j_client import Neo4jClient


def test_client_initialization():
    client = Neo4jClient(
        uri="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )

    assert client.uri == "bolt://localhost:7687"
    assert client.username == "neo4j"


def test_connect_and_close(monkeypatch):

    class FakeDriver:
        def close(self):
            pass

    class FakeGraphDatabase:
        @staticmethod
        def driver(uri, auth):
            return FakeDriver()

    monkeypatch.setattr(
        "database.neo4j_client.GraphDatabase",
        FakeGraphDatabase
    )

    client = Neo4jClient()

    client.connect()

    assert client.driver is not None

    client.close()

    assert client.driver is None