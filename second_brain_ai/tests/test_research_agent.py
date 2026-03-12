import pytest

from agents.research_agent import ResearchAgent


class MockGemini:
    async def generate_research(self, payload):
        return {
            "concept": payload["concept"],
            "domain": payload["domain"],
            "explanation": "Test explanation",
            "key_points": [],
            "related_concepts": [],
            "references": []
        }


@pytest.mark.asyncio
async def test_research_agent():

    agent = ResearchAgent()

    agent.ai_service = MockGemini()

    result = await agent.run({
        "concept": "Test Concept",
        "domain": "Test Domain"
    })

    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_missing_payload():

    agent = ResearchAgent()

    result = await agent.run({})

    assert result["status"] == "error"