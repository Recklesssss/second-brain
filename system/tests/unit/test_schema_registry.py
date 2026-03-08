import tempfile
import yaml
from core.schema_loader.schema_registry import SchemaRegistry


def test_schema_loading():

    schema_data = {
        "memory": {"fields": ["id", "content"]},
        "agent": {"fields": ["name", "role"]}
    }

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        yaml.dump(schema_data, f)
        file_path = f.name

    registry = SchemaRegistry(file_path)
    registry.load()

    assert "memory" in registry.list_schemas()
    assert registry.get_schema("agent") is not None