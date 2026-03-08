from ai.prompt_manager import PromptManager


def test_prompt_manager_initialization():
    manager = PromptManager()
    assert manager is not None


def test_build_prompt():
    manager = PromptManager()

    prompt = manager.build_prompt(
        system_prompt="You are a helpful assistant",
        user_prompt="Explain gravity",
        context="Physics discussion"
    )

    assert "System:" in prompt
    assert "User:" in prompt
    assert "Context:" in prompt


def test_generate_response_method_exists():
    manager = PromptManager()
    assert hasattr(manager, "generate_response")


def test_memory_prompt_builder():
    manager = PromptManager()

    prompt = manager.build_memory_prompt(
        "What did we discuss earlier?",
        ["User likes physics", "User studying relativity"]
    )

    assert "memory context" in prompt.lower()