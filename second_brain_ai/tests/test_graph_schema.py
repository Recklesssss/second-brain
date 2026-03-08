import pytest
from database.graph_schema import GraphSchemaInitializer


def test_initializer_creation():
    schema = GraphSchemaInitializer()
    assert schema is not None


def test_relationship_validation():
    schema = GraphSchemaInitializer()

    schema.validate_relationship_type("related_to")

    with pytest.raises(ValueError):
        schema.validate_relationship_type("invalid_relationship")