from core.knowledge_graph import KnowledgeGraphService


def test_graph_service_creation():

    service = KnowledgeGraphService()

    assert service is not None


def test_node_validation():

    service = KnowledgeGraphService()

    try:
        service._validate_node_type("InvalidType")
        assert False
    except ValueError:
        assert True