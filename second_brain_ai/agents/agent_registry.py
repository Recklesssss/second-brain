import logging
from typing import Dict, Type

from second_brain_ai.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for all AI agents.

    Allows dynamic registration and lookup of agents.
    """

    def __init__(self):
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        """
        Register an agent class.
        """

        if name in self._agents:
            logger.warning(f"Agent '{name}' already registered")

        if not issubclass(agent_cls, BaseAgent):
            raise TypeError("Agent must inherit from BaseAgent")

        self._agents[name] = agent_cls

        logger.info(f"Agent registered: {name}")

    def get(self, name: str) -> Type[BaseAgent]:
        """
        Retrieve an agent class by name.
        """

        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found")

        return self._agents[name]

    def list_agents(self):
        """
        Return list of registered agents.
        """

        return list(self._agents.keys())