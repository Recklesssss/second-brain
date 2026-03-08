import yaml
from pathlib import Path
from core.logging.get_logger import get_logger

logger = get_logger(__name__)


class SchemaRegistry:

    def __init__(self, schema_path: str):
        self.schema_path = Path(schema_path)
        self.schemas = {}

    def load(self):
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        with open(self.schema_path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Schema registry must contain dictionary structure")

        self.schemas = data
        logger.info(f"Schemas loaded: {len(self.schemas)}")

    def get_schema(self, name: str):
        return self.schemas.get(name)

    def list_schemas(self):
        return list(self.schemas.keys())