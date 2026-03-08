import pytest

from database.graph_schema import GraphSchemaInitializer


class FakeClient:

    def __init__(self):
        self.queries = []

    def connect(self):
        pass

    def run_query(self, query, params=None):
        self.queries.append((query, params))
        return []

    def close(self):
        pass


def test_schema_loader(monkeypatch):

    initializer = GraphSchemaInitializer()

    fake = FakeClient()

    initializer.client = fake

    initializer.initialize()

    assert len(fake.queries) > 0