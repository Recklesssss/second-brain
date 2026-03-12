from core.memory_system import MemoryStorageService


def test_memory_service_creation():

    service = MemoryStorageService()

    assert service is not None


def test_memory_methods_exist():

    service = MemoryStorageService()

    assert hasattr(service, "store_memory")
    assert hasattr(service, "get_memory")
    assert hasattr(service, "list_memories")
    assert hasattr(service, "delete_memory")