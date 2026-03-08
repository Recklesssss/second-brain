from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    environment: str
    database_url: str
    log_level: str
    api_port: int


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("ENVIRONMENT", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///brain.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        api_port=int(os.getenv("API_PORT", "8000"))
    )


settings = load_settings()