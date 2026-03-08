import os
import pytest
from ai.gemini_service import GeminiService


def test_missing_api_key():
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]

    with pytest.raises(ValueError):
        GeminiService()


def test_service_initialization():
    os.environ["GEMINI_API_KEY"] = "test_key"

    service = GeminiService()

    assert service.api_key == "test_key"


def test_generate_method_exists():
    os.environ["GEMINI_API_KEY"] = "test_key"

    service = GeminiService()

    assert hasattr(service, "generate")