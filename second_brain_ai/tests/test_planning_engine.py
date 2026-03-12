import pytest

from agents.planning_engine import PlanningEngine
from agents.agent_registry import AgentRegistry


@pytest.fixture
def planning_engine():
    registry = AgentRegistry()
    return PlanningEngine(registry)


def test_research_plan(planning_engine):
    payload = {
        "concept": "Neural Networks",
        "domain": "Artificial Intelligence"
    }

    plan = planning_engine.plan("research_concept", payload)

    assert plan["plan_type"] == "research_pipeline"
    assert len(plan["steps"]) == 2
    assert plan["steps"][0]["agent"] == "research_agent"
    assert plan["steps"][1]["agent"] == "question_generator"


def test_learning_plan(planning_engine):
    payload = {
        "concept": "Backpropagation",
        "domain": "Machine Learning"
    }

    plan = planning_engine.plan("learning_module", payload)

    assert plan["plan_type"] == "learning_pipeline"
    assert len(plan["steps"]) == 3
    assert plan["steps"][1]["agent"] == "learning_agent"


def test_idea_plan(planning_engine):
    payload = {
        "concepts": ["Graph Theory", "Neural Networks"]
    }

    plan = planning_engine.plan("idea_generation", payload)

    assert plan["plan_type"] == "idea_pipeline"
    assert plan["steps"][0]["agent"] == "idea_synthesizer"


def test_curriculum_plan(planning_engine):
    payload = {
        "domain": "Machine Learning"
    }

    plan = planning_engine.plan("curriculum_generation", payload)

    assert plan["plan_type"] == "curriculum_pipeline"
    assert plan["steps"][0]["agent"] == "curriculum_builder"


def test_invalid_task(planning_engine):
    with pytest.raises(ValueError):
        planning_engine.plan("invalid_task", {})