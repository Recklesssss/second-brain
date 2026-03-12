from core.interaction_history import InteractionHistoryService


def test_interaction_service_creation():

    service = InteractionHistoryService()

    assert service is not None


def test_interaction_methods_exist():

    service = InteractionHistoryService()

    assert hasattr(service, "record_interaction")
    assert hasattr(service, "get_interaction")
    assert hasattr(service, "get_user_history")
    assert hasattr(service, "delete_interaction")