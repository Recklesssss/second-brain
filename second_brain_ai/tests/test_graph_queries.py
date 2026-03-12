from core.graph_queries import GraphQueryService


def test_query_service_creation():

    service = GraphQueryService()

    assert service is not None


def test_query_methods_exist():

    service = GraphQueryService()

    assert hasattr(service, "get_related_concepts")
    assert hasattr(service, "get_domain_concepts")
    assert hasattr(service, "get_dependencies")
    assert hasattr(service, "find_concept_by_name")