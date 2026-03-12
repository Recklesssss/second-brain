import os
from pathlib import Path
from functools import lru_cache
from typing import Optional


class Settings:
    """
    Central configuration object.

    Reads environment variables and exposes them as attributes.
    """

    def __init__(self) -> None:

        # Application
        self.app_name: str = os.getenv("APP_NAME", "ai_second_brain")
        self.environment: str = os.getenv("ENVIRONMENT", "development")

        # Neo4j
        self.neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password: Optional[str] = os.getenv("NEO4J_PASSWORD")

        # AI Services
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.notebooklm_api_key: Optional[str] = os.getenv("NOTEBOOKLM_API_KEY")

        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

        # Project root
        self.project_root: Path = Path(os.getenv("PROJECT_ROOT", Path.cwd()))

        # Config files
        self.schema_registry_path: Path = self.project_root / "SCHEMA_REGISTRY.yaml"
        self.prompt_library_path: Path = self.project_root / "PROMPT_LIBRARY.yaml"

    def validate(self) -> None:
        """
        Validate required configuration values.
        """

        required = {
            "NEO4J_URI": self.neo4j_uri,
            "NEO4J_USER": self.neo4j_user,
        }

        missing = [k for k, v in required.items() if v is None]

        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

    def to_dict(self) -> dict:
        """
        Convert settings to dictionary.
        """
        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "neo4j_uri": self.neo4j_uri,
            "neo4j_user": self.neo4j_user,
            "log_level": self.log_level,
        }


@lru_cache
def get_settings() -> Settings:
    """
    Return cached settings instance.
    """
    settings = Settings()
    settings.validate()
    return settings