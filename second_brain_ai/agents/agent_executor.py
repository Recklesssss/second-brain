import logging
from typing import Dict, Any

from second_brain_ai.agents.agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class AgentExecutor:
    """
    Executes registered agents.

    Responsible for retrieving agents from the registry,
    instantiating them, and executing their run method.
    """

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def execute_agent(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered agent by name.
        """

        try:

            agent_cls = self.registry.get(agent_name)

            agent_instance = agent_cls(agent_name)

            logger.info(f"Executing agent: {agent_name}")

            result = await agent_instance.run(payload)

            logger.info(f"Agent execution completed: {agent_name}")

            return result

        except Exception as e:

            logger.exception("Agent execution manager failure")

            return {
                "status": "error",
                "error_code": "AGENT_FAILURE",
                "message": str(e),
                "timestamp": None
            }