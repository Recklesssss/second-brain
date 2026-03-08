from .settings import settings


def validate_environment():
    if settings.environment not in ["development", "production", "test"]:
        raise ValueError("Invalid environment setting")

    if settings.api_port <= 0:
        raise ValueError("Invalid API port")