import yaml
from pathlib import Path
from core.logging.get_logger import get_logger

logger = get_logger(__name__)


class PromptLibrary:

    def __init__(self, prompt_path: str):
        self.prompt_path = Path(prompt_path)
        self.prompts = {}

    def load(self):

        if not self.prompt_path.exists():
            raise FileNotFoundError(f"Prompt library not found: {self.prompt_path}")

        with open(self.prompt_path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Prompt library must be a dictionary")

        self.prompts = data

        logger.info(f"Prompts loaded: {len(self.prompts)}")

    def get_prompt(self, name: str):
        return self.prompts.get(name)

    def format_prompt(self, name: str, **kwargs):

        template = self.get_prompt(name)

        if template is None:
            raise ValueError(f"Prompt not found: {name}")

        return template.format(**kwargs)

    def list_prompts(self):
        return list(self.prompts.keys())