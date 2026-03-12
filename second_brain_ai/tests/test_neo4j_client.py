from database.neo4j_client import Neo4jClient


def test_client_initialization():

    client = Neo4jClient()

    assert client.uri is not None
    assert client.user is not None


def test_client_connect_and_close():

    client = Neo4jClient()

    try:
        client.connect()
        assert client._driver is not None
    finally:
        client.close()