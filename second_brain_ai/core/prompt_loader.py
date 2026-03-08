import yaml
import os


class PromptLibrary:
    """
    Loads and provides access to the global prompt library.
    """

    def __init__(self, prompt_path: str = "config/PROMPT_LIBRARY.yaml"):
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt library not found: {prompt_path}")

        with open(prompt_path, "r") as f:
            self.prompts = yaml.safe_load(f)

        self._validate()

    def _validate(self):
        if "prompt_library" not in self.prompts:
            raise ValueError("Invalid prompt library structure")

        if "agent_prompts" not in self.prompts["prompt_library"]:
            raise ValueError("Missing agent_prompts section")

    def get_system_prompt(self, name: str):
        return self.prompts["prompt_library"]["system_prompts"].get(name)

    def get_agent_prompt(self, agent: str, prompt_name: str):
        return (
            self.prompts["prompt_library"]
            .get("agent_prompts", {})
            .get(agent, {})
            .get(prompt_name)
        )

    def format_prompt(self, template: str, **kwargs):
        """
        Replace variables inside prompt templates.
        """
        return template.format(**kwargs)

    def raw(self):
        return self.prompts