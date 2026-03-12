import pytest
from agents.idea_synthesizer import IdeaSynthesizerAgent


class MockGemini:
    async def generate_idea(self, concepts):
        return {
            "title": "New Idea",
            "description": "Generated idea from concepts",
            "related_concepts": [c["name"] for c in concepts],
            "potential_applications": ["Education", "Research"]
        }


@pytest.mark.asyncio
async def test_idea_generation():
    agent = IdeaSynthesizerAgent()
    agent.ai_service = MockGemini()

    concepts = [{"name": "Concept A"}, {"name": "Concept B"}]
    result = await agent.run({"concepts": concepts})

    assert result["status"] == "success"
    assert "idea_title" in result["data"]


@pytest.mark.asyncio
async def test_invalid_payload():
    agent = IdeaSynthesizerAgent()
    result = await agent.run({})
    assert result["status"] == "error"