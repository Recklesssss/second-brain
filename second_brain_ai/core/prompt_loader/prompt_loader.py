from pathlib import Path
from functools import lru_cache
from typing import Dict, Any
import yaml

from second_brain_ai.config.settings import get_settings


class PromptLibraryLoader:
    """
    Loader for PROMPT_LIBRARY.yaml.
    """

    REQUIRED_TOP_LEVEL_FIELDS = [
        "prompt_library",
        "system_prompts",
        "agent_prompts",
    ]

    def __init__(self, prompt_path: Path | None = None):

        settings = get_settings()

        self.prompt_path = prompt_path or settings.prompt_library_path
        self._prompt_data: Dict[str, Any] | None = None

    def load(self) -> Dict[str, Any]:

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt library not found: {self.prompt_path}"
            )

        with open(self.prompt_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._validate(data)

        self._prompt_data = data
        return data

    def _validate(self, data: Dict[str, Any]):

        missing = [
            field
            for field in self.REQUIRED_TOP_LEVEL_FIELDS
            if field not in data
        ]

        if missing:
            raise ValueError(
                f"Invalid prompt library. Missing fields: {missing}"
            )

    def get_agent_prompt(self, agent_name: str, prompt_name: str) -> str:

        if self._prompt_data is None:
            self.load()

        return self._prompt_data["agent_prompts"][agent_name][prompt_name]

    def get_system_prompt(self, name: str) -> str:

        if self._prompt_data is None:
            self.load()

        return self._prompt_data["system_prompts"][name]


@lru_cache
def get_prompt_library() -> PromptLibraryLoader:
    """
    Cached prompt library loader.
    """

    loader = PromptLibraryLoader()
    loader.load()
    return loader