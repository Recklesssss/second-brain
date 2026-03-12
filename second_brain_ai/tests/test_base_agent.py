import pytest

from agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):

    async def execute(self, payload):

        return self.success_response({
            "message": "executed"
        })


@pytest.mark.asyncio
async def test_agent_execution():

    agent = DummyAgent("dummy_agent")

    result = await agent.run({})

    assert result["status"] == "success"
    assert "data" in result


@pytest.mark.asyncio
async def test_error_response():

    agent = DummyAgent("dummy")

    error = agent.error_response("TEST_ERROR", "failure")

    assert error["status"] == "error"
    assert error["error_code"] == "TEST_ERROR"