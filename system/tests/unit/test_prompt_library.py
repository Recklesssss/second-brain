import tempfile
import yaml
from core.prompt_loader.prompt_library import PromptLibrary


def test_prompt_loading():

    prompts = {
        "test_prompt": "Hello {name}"
    }

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        yaml.dump(prompts, f)
        path = f.name

    library = PromptLibrary(path)
    library.load()

    assert "test_prompt" in library.list_prompts()


def test_prompt_formatting():

    prompts = {
        "greet": "Hello {name}"
    }

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        yaml.dump(prompts, f)
        path = f.name

    library = PromptLibrary(path)
    library.load()

    result = library.format_prompt("greet", name="AI")

    assert result == "Hello AI"