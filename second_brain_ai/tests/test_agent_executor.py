import pytest

from agents.agent_registry import AgentRegistry
from agents.agent_executor import AgentExecutor
from agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):

    async def execute(self, payload):

        return self.success_response({"executed": True})


@pytest.mark.asyncio
async def test_execute_agent():

    registry = AgentRegistry()

    registry.register("dummy", DummyAgent)

    executor = AgentExecutor(registry)

    result = await executor.execute_agent("dummy", {})

    assert result["status"] == "success"
    assert result["data"]["executed"] is True


@pytest.mark.asyncio
async def test_missing_agent():

    registry = AgentRegistry()

    executor = AgentExecutor(registry)

    result = await executor.execute_agent("unknown", {})

    assert result["status"] == "error"