import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base interface for all AI agents in the system.

    All agents must inherit from this class and implement
    the execute() method.

    Responsibilities:

    - Receive structured task payload
    - Execute reasoning using AI services
    - Return schema compliant response
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    @abstractmethod
    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic.

        Parameters
        ----------
        payload : dict
            Input data required by the agent

        Returns
        -------
        dict
            API schema compliant response
        """
        pass

    def success_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate standardized success response.
        """

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def error_response(self, error_code: str, message: str) -> Dict[str, Any]:
        """
        Generate standardized error response.
        """

        logger.error(f"{self.agent_name} error: {message}")

        return {
            "status": "error",
            "error_code": error_code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safe execution wrapper used by orchestrators.
        """

        try:

            logger.info(f"Agent {self.agent_name} started execution")

            result = await self.execute(payload)

            logger.info(f"Agent {self.agent_name} completed execution")

            return result

        except Exception as e:

            logger.exception("Agent execution failure")

            return self.error_response(
                "AGENT_FAILURE",
                str(e)
            )