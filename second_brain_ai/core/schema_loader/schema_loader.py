from pathlib import Path
from functools import lru_cache
from typing import Any, Dict
import yaml

from second_brain_ai.config.settings import get_settings


class SchemaRegistryLoader:
    """
    Loads and validates SCHEMA_REGISTRY.yaml.
    """

    REQUIRED_TOP_LEVEL_FIELDS = [
        "schema_registry",
        "graph_schema",
        "api_schema",
        "error_codes",
        "prompt_templates",
        "agent_message_protocol",
        "logging_schema",
    ]

    def __init__(self, schema_path: Path | None = None):

        settings = get_settings()

        self.schema_path = schema_path or settings.schema_registry_path
        self._schema_data: Dict[str, Any] | None = None

    def load(self) -> Dict[str, Any]:

        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema registry not found: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._validate(data)

        self._schema_data = data
        return data

    def _validate(self, data: Dict[str, Any]) -> None:

        missing = [
            field
            for field in self.REQUIRED_TOP_LEVEL_FIELDS
            if field not in data
        ]

        if missing:
            raise ValueError(f"Invalid schema registry. Missing fields: {missing}")

    def get_graph_schema(self) -> Dict[str, Any]:

        if self._schema_data is None:
            self.load()

        return self._schema_data["graph_schema"]

    def get_api_schema(self) -> Dict[str, Any]:

        if self._schema_data is None:
            self.load()

        return self._schema_data["api_schema"]

    def get_error_codes(self) -> Dict[str, Any]:

        if self._schema_data is None:
            self.load()

        return self._schema_data["error_codes"]


@lru_cache
def get_schema_registry() -> SchemaRegistryLoader:
    """
    Cached schema loader instance.
    """
    loader = SchemaRegistryLoader()
    loader.load()
    return loader