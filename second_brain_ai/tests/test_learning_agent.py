import pytest

from agents.learning_agent import LearningAgent


class MockGemini:

    async def generate_learning_module(self, payload):

        return {
            "concept": payload["concept_data"].get("concept"),
            "summary": "Example summary",
            "examples": [],
            "analogies": [],
            "practice_exercises": []
        }


@pytest.mark.asyncio
async def test_learning_agent():

    agent = LearningAgent()

    agent.ai_service = MockGemini()

    result = await agent.run({
        "concept_data": {"concept": "Test"},
        "user_profile": {"style": "visual"}
    })

    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_invalid_payload():

    agent = LearningAgent()

    result = await agent.run({})

    assert result["status"] == "error"