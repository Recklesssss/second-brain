import requests
from typing import Optional, Dict, Any

from config.settings import get_settings
from core.logging import get_logger


logger = get_logger(__name__)


class GeminiService:
    """
    Wrapper for Google Gemini API.
    """

    def __init__(self):

        settings = get_settings()

        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_text(
        self,
        prompt: str,
        model: str = "gemini-pro",
        temperature: float = 0.7,
    ) -> Optional[str]:

        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"

        payload: Dict[str, Any] = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature
            }
        }

        try:

            response = requests.post(url, json=payload)

            response.raise_for_status()

            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:

            logger.error(f"Gemini API error: {e}")

            return None