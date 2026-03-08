import yaml
import os


class SchemaRegistryLoader:
    """
    Loads and validates the global schema registry.
    """

    def __init__(self, schema_path: str = "config/SCHEMA_REGISTRY.yaml"):
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r") as f:
            self.schema = yaml.safe_load(f)

        self._validate_schema()

    def _validate_schema(self):
        if "schema_registry" not in self.schema:
            raise ValueError("Invalid schema registry format")

        if "graph_schema" not in self.schema["schema_registry"]:
            raise ValueError("Missing graph_schema definition")

    def get_node_labels(self):
        return self.schema["schema_registry"]["graph_schema"]["node_labels"]

    def get_relationship_types(self):
        return self.schema["schema_registry"]["graph_schema"]["relationship_types"]

    def get_constraints(self):
        return self.schema["schema_registry"]["graph_schema"]["constraints"]

    def get_api_schema(self):
        return self.schema["schema_registry"]["api_schema"]

    def get_error_codes(self):
        return self.schema["schema_registry"]["error_codes"]

    def get_logging_schema(self):
        return self.schema["schema_registry"]["logging_schema"]

    def raw(self):
        return self.schema