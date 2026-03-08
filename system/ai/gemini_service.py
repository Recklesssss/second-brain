import os
import yaml
import logging
import google.generativeai as genai
from pathlib import Path


class GeminiService:
    """
    Wrapper around Google Gemini API used by AI agents.
    Handles prompt execution using PROMPT_LIBRARY.yaml.
    """

    def __init__(self, prompt_library_path="config/prompt_library.yaml"):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-pro")

        self.prompt_library = self._load_prompt_library(prompt_library_path)

    def _load_prompt_library(self, path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Prompt library not found: {path}")

        with open(path) as f:
            return yaml.safe_load(f)


    def generate(self, prompt: str, temperature: float = 0.3):

        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature
            }
        )

        return response.text

    def run_prompt(self, prompt_name: str, variables: dict):

        prompts = self.prompt_library["prompt_library"]

        if prompt_name not in prompts:
            raise ValueError(f"Prompt not found: {prompt_name}")

        template = prompts[prompt_name]["template"]

        prompt = template.format(**variables)

        return self.generate(prompt)
    
    def generate_json(self, prompt: str):

        formatted_prompt = f"""
Return ONLY valid JSON.

{prompt}
"""

        response = self.generate(formatted_prompt)

        return response