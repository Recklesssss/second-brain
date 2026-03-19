import yaml
from pathlib import Path
from typing import Dict, Any
from core.logger import error_log

class SchemaValidator:
    """Validates node schemas dynamically against SCHEMA_REGISTRY.yaml."""
    def __init__(self):
        schema_path = Path(__file__).resolve().parent.parent / "SCHEMA_REGISTRY.yaml"
        try:
            with open(schema_path, "r") as f:
                self.registry = yaml.safe_load(f).get("schema_definitions", {})
        except Exception as e:
            error_log.error(f"Failed to load SCHEMA_REGISTRY: {e}")
            self.registry = {"nodes": {}, "relationships": {}}

    def validate_node(self, label: str, data: Dict[str, Any]) -> bool:
        nodes = self.registry.get("nodes", {})
        if label not in nodes:
            error_log.error(f"Validation failed: Unknown node label {label}")
            return False
            
        required_props = nodes[label].get("properties", {})
        for prop in required_props.keys():
            if prop not in data:
                error_log.error(f"Validation failed: Missing property {prop} on {label}")
                return False
                
        return True

validator = SchemaValidator()
