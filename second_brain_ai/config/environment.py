from functools import lru_cache
from .settings import Settings


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.

    Using caching ensures environment variables are only loaded once
    during application lifecycle.
    """
    return Settings()