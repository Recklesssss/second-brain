import pytest
from core.schema_loader import SchemaRegistryLoader


def test_schema_load():
    loader = SchemaRegistryLoader("config/SCHEMA_REGISTRY.yaml")
    assert loader.raw() is not None


def test_node_labels():
    loader = SchemaRegistryLoader("config/SCHEMA_REGISTRY.yaml")
    labels = loader.get_node_labels()
    assert "Concept" in labels


def test_relationship_types():
    loader = SchemaRegistryLoader("config/SCHEMA_REGISTRY.yaml")
    rels = loader.get_relationship_types()
    assert "related_to" in rels


def test_constraints():
    loader = SchemaRegistryLoader("config/SCHEMA_REGISTRY.yaml")
    constraints = loader.get_constraints()
    assert "enforce_unique_node_ids" in constraints