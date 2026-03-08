import pytest
from core.prompt_loader import PromptLibrary


def test_prompt_library_load():
    loader = PromptLibrary("config/PROMPT_LIBRARY.yaml")
    assert loader.raw() is not None


def test_system_prompt_access():
    loader = PromptLibrary("config/PROMPT_LIBRARY.yaml")
    prompt = loader.get_system_prompt("agent_system_prefix")
    assert prompt is not None


def test_agent_prompt_access():
    loader = PromptLibrary("config/PROMPT_LIBRARY.yaml")
    prompt = loader.get_agent_prompt("research_agent", "concept_research")
    assert prompt is not None


def test_prompt_formatting():
    loader = PromptLibrary("config/PROMPT_LIBRARY.yaml")
    template = "Hello {name}"
    result = loader.format_prompt(template, name="AI")
    assert result == "Hello AI"