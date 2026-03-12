import tempfile
from pathlib import Path
import yaml

from core.prompt_loader.prompt_loader import PromptLibraryLoader


VALID_PROMPT_LIBRARY = {
    "prompt_library": {},
    "system_prompts": {
        "agent_system_prefix": "prefix"
    },
    "agent_prompts": {
        "research_agent": {
            "concept_research": "prompt"
        }
    }
}


def test_prompt_loader_valid():

    with tempfile.TemporaryDirectory() as tmp:

        path = Path(tmp) / "PROMPT_LIBRARY.yaml"

        with open(path, "w") as f:
            yaml.dump(VALID_PROMPT_LIBRARY, f)

        loader = PromptLibraryLoader(prompt_path=path)

        data = loader.load()

        assert data is not None


def test_prompt_loader_validation():

    with tempfile.TemporaryDirectory() as tmp:

        path = Path(tmp) / "PROMPT_LIBRARY.yaml"

        invalid = VALID_PROMPT_LIBRARY.copy()
        invalid.pop("system_prompts")

        with open(path, "w") as f:
            yaml.dump(invalid, f)

        loader = PromptLibraryLoader(prompt_path=path)

        try:
            loader.load()
            assert False
        except ValueError:
            assert True