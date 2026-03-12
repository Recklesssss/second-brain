import pytest

from agents.agent_registry import AgentRegistry
from agents.base_agent import BaseAgent


class DummyAgent(BaseAgent):

    async def execute(self, payload):
        return self.success_response({"ok": True})


def test_register_agent():

    registry = AgentRegistry()

    registry.register("dummy", DummyAgent)

    assert "dummy" in registry.list_agents()


def test_get_agent():

    registry = AgentRegistry()

    registry.register("dummy", DummyAgent)

    agent_cls = registry.get("dummy")

    assert issubclass(agent_cls, BaseAgent)


def test_missing_agent():

    registry = AgentRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown")