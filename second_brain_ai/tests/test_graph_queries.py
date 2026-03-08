from core.graph_queries import GraphQueryUtilities


def test_graph_queries_initialization():
    gq = GraphQueryUtilities()
    assert gq is not None


def test_methods_exist():
    gq = GraphQueryUtilities()

    assert hasattr(gq, "get_related_concepts")
    assert hasattr(gq, "get_dependencies")
    assert hasattr(gq, "get_concepts_in_domain")
    assert hasattr(gq, "find_shortest_path")