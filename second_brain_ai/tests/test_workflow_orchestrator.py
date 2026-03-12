import pytest
from unittest.mock import MagicMock

from agents.workflow_orchestrator import AgentWorkflowOrchestrator
from agents.planning_engine import PlanningEngine
from agents.agent_registry import AgentRegistry


class DummyExecutor:
    def execute(self, agent_name, action, payload):
        return {
            "agent": agent_name,
            "action": action,
            "status": "ok"
        }


@pytest.fixture
def orchestrator():

    registry = AgentRegistry()
    planner = PlanningEngine(registry)

    executor = DummyExecutor()

    return AgentWorkflowOrchestrator(planner, executor)


def test_research_workflow(orchestrator):

    payload = {
        "concept": "Transformers",
        "domain": "AI"
    }

    result = orchestrator.execute_workflow("research_concept", payload)

    assert result["plan_type"] == "research_pipeline"
    assert result["steps_executed"] == 2


def test_learning_workflow(orchestrator):

    payload = {
        "concept": "Gradient Descent",
        "domain": "ML"
    }

    result = orchestrator.execute_workflow("learning_module", payload)

    assert result["plan_type"] == "learning_pipeline"
    assert result["steps_executed"] == 3