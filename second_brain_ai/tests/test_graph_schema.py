from database.graph_schema import GraphSchemaInitializer


def test_schema_initializer_creation():

    initializer = GraphSchemaInitializer()

    assert initializer is not None


def test_initialize_methods_exist():

    initializer = GraphSchemaInitializer()

    assert hasattr(initializer, "initialize_constraints")
    assert hasattr(initializer, "initialize_indexes")