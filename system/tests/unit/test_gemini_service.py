import pytest
from ai.gemini_service import GeminiService


class FakeModel:

    def generate_content(self, prompt, generation_config=None):

        class Response:
            text = "test response"

        return Response()


def test_generate(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "test")

    service = GeminiService()

    service.model = FakeModel()

    result = service.generate("Hello")

    assert result == "test response"


def test_prompt_execution(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "test")

    service = GeminiService()

    service.model = FakeModel()

    service.prompt_library = {
        "prompt_library": {
            "test_prompt": {
                "template": "Hello {name}"
            }
        }
    }

    result = service.run_prompt("test_prompt", {"name": "AI"})

    assert result == "test response"