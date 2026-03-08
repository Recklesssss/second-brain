import pytest
from core.knowledge_graph import KnowledgeGraphService


def test_service_initialization():
    kg = KnowledgeGraphService()
    assert kg is not None


def test_invalid_node_label():
    kg = KnowledgeGraphService()

    with pytest.raises(ValueError):
        kg.create_node("InvalidLabel", {"id": "1"})


def test_invalid_relationship():
    kg = KnowledgeGraphService()

    with pytest.raises(ValueError):
        kg.create_relationship(
            "Concept",
            "1",
            "Concept",
            "2",
            "invalid_relation"
        )


def test_query_method_exists():
    kg = KnowledgeGraphService()
    assert hasattr(kg, "query")