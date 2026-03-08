from core.config.settings import load_settings


def test_settings_load():
    settings = load_settings()

    assert settings.environment is not None
    assert settings.database_url is not None
    assert settings.api_port > 0