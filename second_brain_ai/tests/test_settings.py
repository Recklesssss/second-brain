import os
from second_brain_ai.config.settings import Settings


def test_settings_defaults():

    settings = Settings()

    assert settings.app_name == "ai_second_brain"
    assert settings.environment in ["development", "production", "test", "development"]


def test_settings_to_dict():

    settings = Settings()

    data = settings.to_dict()

    assert "app_name" in data
    assert "environment" in data
    assert isinstance(data, dict)


def test_settings_validation():

    os.environ["NEO4J_URI"] = "bolt://localhost:7687"
    os.environ["NEO4J_USER"] = "neo4j"

    settings = Settings()

    settings.validate()