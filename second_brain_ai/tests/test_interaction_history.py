from core.interaction_history import InteractionHistoryService


def test_interaction_service_initialization():
    service = InteractionHistoryService()
    assert service is not None


def test_create_session_method_exists():
    service = InteractionHistoryService()
    assert hasattr(service, "create_session")


def test_record_interaction_method_exists():
    service = InteractionHistoryService()
    assert hasattr(service, "record_interaction")


def test_store_message_method_exists():
    service = InteractionHistoryService()
    assert hasattr(service, "store_message")


def test_get_session_history_method_exists():
    service = InteractionHistoryService()
    assert hasattr(service, "get_session_history")