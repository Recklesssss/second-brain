import pytest

from agents.question_generator import QuestionGenerator


class MockGemini:

    async def generate_questions(self, concept_data):

        return {
            "concept": concept_data.get("concept", "Test"),
            "basic_questions": ["What is the concept?"],
            "advanced_questions": ["Explain deeper implications."],
            "reflection_prompts": ["How would you apply this?"]
        }


@pytest.mark.asyncio
async def test_question_generation():

    agent = QuestionGenerator()

    agent.ai_service = MockGemini()

    result = await agent.run({
        "concept_data": {"concept": "Test Concept"}
    })

    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_missing_payload():

    agent = QuestionGenerator()

    result = await agent.run({})

    assert result["status"] == "error"