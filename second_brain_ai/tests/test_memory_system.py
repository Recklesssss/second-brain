from core.memory_system import MemoryStorageService


def test_memory_service_initialization():
    memory = MemoryStorageService()
    assert memory is not None


def test_store_memory_method_exists():
    memory = MemoryStorageService()
    assert hasattr(memory, "store_memory")


def test_get_memory_method_exists():
    memory = MemoryStorageService()
    assert hasattr(memory, "get_memory_by_id")


def test_link_memory_method_exists():
    memory = MemoryStorageService()
    assert hasattr(memory, "link_memory")