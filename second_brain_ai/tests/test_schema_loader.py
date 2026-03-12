import tempfile
from pathlib import Path
import yaml

from core.schema_loader.schema_loader import SchemaRegistryLoader


VALID_SCHEMA = {
    "schema_registry": {},
    "graph_schema": {},
    "api_schema": {},
    "error_codes": {},
    "prompt_templates": {},
    "agent_message_protocol": {},
    "logging_schema": {},
}


def test_schema_loader_valid():

    with tempfile.TemporaryDirectory() as tmp:

        path = Path(tmp) / "SCHEMA_REGISTRY.yaml"

        with open(path, "w") as f:
            yaml.dump(VALID_SCHEMA, f)

        loader = SchemaRegistryLoader(schema_path=path)

        schema = loader.load()

        assert schema is not None


def test_schema_validation_missing_field():

    with tempfile.TemporaryDirectory() as tmp:

        path = Path(tmp) / "SCHEMA_REGISTRY.yaml"

        invalid = VALID_SCHEMA.copy()
        invalid.pop("api_schema")

        with open(path, "w") as f:
            yaml.dump(invalid, f)

        loader = SchemaRegistryLoader(schema_path=path)

        try:
            loader.load()
            assert False
        except ValueError:
            assert True