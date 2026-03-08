import os
import time
import requests
from core.logging.logger import LoggerFactory


class GeminiService:
    """
    Wrapper for Gemini API interactions.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("gemini_service")

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = os.getenv(
            "GEMINI_API_URL",
            "https://generativelanguage.googleapis.com/v1beta/models"
        )

        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

    def generate(self, prompt: str, max_retries: int = 3):
        """
        Send prompt to Gemini model and return response.
        """

        endpoint = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()

                    return data["candidates"][0]["content"]["parts"][0]["text"]

                self.logger.warning(
                    f"Gemini API error: {response.status_code} {response.text}"
                )

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Gemini request failed: {str(e)}")

            time.sleep(2 ** attempt)

        raise RuntimeError("Gemini API request failed after retries")