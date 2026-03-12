import pytest
from agents.curriculum_builder import CurriculumBuilderAgent


class MockKG:
    def get_concepts(self, domain):
        return [
            {"name": "Concept A", "prerequisites": []},
            {"name": "Concept B", "prerequisites": [{"name": "Concept A"}]},
        ]


@pytest.mark.asyncio
async def test_curriculum_generation():
    agent = CurriculumBuilderAgent()
    agent.kg_client = MockKG()
    payload = {"domain": "Science"}
    result = await agent.run(payload)

    assert result["status"] == "success"
    assert "learning_sequence" in result["data"]
    assert "prerequisite_graph" in result["data"]


@pytest.mark.asyncio
async def test_missing_domain():
    agent = CurriculumBuilderAgent()
    result = await agent.run({})
    assert result["status"] == "error"