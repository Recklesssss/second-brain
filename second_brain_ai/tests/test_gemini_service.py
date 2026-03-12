from services.gemini_service import GeminiService


def test_service_creation():

    service = GeminiService()

    assert service is not None


def test_generate_text_method_exists():

    service = GeminiService()

    assert hasattr(service, "generate_text")