from config.environment import get_settings


def test_settings_load():
    settings = get_settings()

    assert settings.APP_NAME is not None
    assert settings.NEO4J_URI.startswith("bolt://")
    assert isinstance(settings.LOG_LEVEL, str)