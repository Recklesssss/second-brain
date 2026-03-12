import pytest
from agents.thinking_engine import ThinkingEngineAgent


class MockGraphUtils:
    def detect_patterns(self, graph_summary):
        return ["pattern1", "pattern2"]

    def identify_gaps(self, graph_summary):
        return ["gap1"]

    def generate_insights(self, graph_summary):
        return ["insight1", "insight2"]


@pytest.mark.asyncio
async def test_thinking_engine_analysis():
    agent = ThinkingEngineAgent()
    agent.graph_utils = MockGraphUtils()

    payload = {"graph_summary": {"nodes": [], "edges": []}}
    result = await agent.run(payload)

    assert result["status"] == "success"
    assert "patterns" in result["data"]
    assert "knowledge_gaps" in result["data"]
    assert "insights" in result["data"]


@pytest.mark.asyncio
async def test_missing_graph_summary():
    agent = ThinkingEngineAgent()
    result = await agent.run({})
    assert result["status"] == "error"