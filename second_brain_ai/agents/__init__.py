"""
Agent module.

Contains all AI agents used in the platform.
"""

from .agent_registry import AgentRegistry
from .research_agent import ResearchAgent
from .learning_agent import LearningAgent
from .idea_synthesizer import IdeaSynthesizerAgent
from .question_generator import QuestionGenerator
from .knowledge_graph_agent import KnowledgeGraphAgent
from .curriculum_builder import CurriculumBuilderAgent
from .thinking_engine import ThinkingEngineAgent
from .planning_engine import PlanningEngine
from .agent_executor import AgentExecutor


def create_agent_registry() -> AgentRegistry:
    """Create and populate the agent registry."""
    registry = AgentRegistry()

    # Register all agents
    registry.register("research_agent", ResearchAgent)
    registry.register("learning_agent", LearningAgent)
    registry.register("idea_synthesizer_agent", IdeaSynthesizerAgent)
    registry.register("question_generator", QuestionGenerator)
    registry.register("knowledge_graph_agent", KnowledgeGraphAgent)
    registry.register("curriculum_builder_agent", CurriculumBuilderAgent)
    registry.register("thinking_engine_agent", ThinkingEngineAgent)
    registry.register("planning_engine", PlanningEngine)

    return registry


# Global registry instance
_agent_registry = None

def get_agent_registry() -> AgentRegistry:
    """Get the global agent registry."""
    global _agent_registry
    if _agent_registry is None:
        _agent_registry = create_agent_registry()
    return _agent_registry

def get_agent_executor() -> AgentExecutor:
    """Get an agent executor instance."""
    registry = get_agent_registry()
    return AgentExecutor(registry)