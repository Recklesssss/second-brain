import os
from dotenv import load_dotenv


class EnvironmentConfig:
    """
    Central configuration loader for AI Second Brain Platform
    """

    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)

    @staticmethod
    def get(key: str, default=None):
        return os.getenv(key, default)

    @staticmethod
    def require(key: str):
        value = os.getenv(key)
        if value is None:
            raise EnvironmentError(f"Missing required environment variable: {key}")
        return value

    @staticmethod
    def get_int(key: str, default: int = None):
        value = os.getenv(key)
        if value is None:
            return default
        return int(value)

    @staticmethod
    def get_bool(key: str, default: bool = False):
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ["true", "1", "yes"]