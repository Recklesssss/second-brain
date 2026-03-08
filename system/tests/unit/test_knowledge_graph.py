import pytest
from core.knowledge_graph import KnowledgeGraph


class FakeClient:

    def __init__(self):
        self.queries = []

    def connect(self):
        pass

    def run_query(self, query, params=None):
        self.queries.append((query, params))
        return [{"n": {"id": "1"}}]

    def close(self):
        pass


def test_create_node(monkeypatch):

    kg = KnowledgeGraph()

    fake = FakeClient()

    kg.client = fake

    kg.create_node("Concept", {"id": "1", "name": "AI"})

    assert len(fake.queries) == 1


def test_get_node(monkeypatch):

    kg = KnowledgeGraph()

    fake = FakeClient()

    kg.client = fake

    node = kg.get_node("Concept", "1")

    assert node is not None


def test_create_relationship(monkeypatch):

    kg = KnowledgeGraph()

    fake = FakeClient()

    kg.client = fake

    kg.create_relationship(
        "Concept",
        "1",
        "RELATED_TO",
        "Concept",
        "2"
    )

    assert len(fake.queries) == 1