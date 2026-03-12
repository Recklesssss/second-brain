from typing import Dict, List, Any
from datetime import datetime

from agents.base_agent import BaseAgent
from agents.agent_registry import AgentRegistry


class PlanningEngine(BaseAgent):
    """
    The Planning Engine is responsible for high-level orchestration planning.

    It analyzes incoming requests and determines which agents should
    execute and in what order.

    It does NOT execute agents directly. Execution is delegated
    to the AgentExecutionManager.
    """

    def __init__(self, agent_registry: AgentRegistry):
        super().__init__(agent_name="planning_engine")
        self.agent_registry = agent_registry

    def plan(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a deterministic plan for agent execution.

        Parameters
        ----------
        task_type : str
            Type of high-level task requested.
        payload : dict
            Task payload.

        Returns
        -------
        Dict
            Execution plan containing ordered agent steps.
        """

        if task_type == "research_concept":
            return self._plan_research(payload)

        if task_type == "learning_module":
            return self._plan_learning(payload)

        if task_type == "idea_generation":
            return self._plan_idea_synthesis(payload)

        if task_type == "curriculum_generation":
            return self._plan_curriculum(payload)

        raise ValueError(f"Unknown task_type: {task_type}")

    def _plan_research(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan for researching a concept.
        """

        steps = [
            {
                "step": 1,
                "agent": "research_agent",
                "action": "concept_research",
                "payload": payload
            },
            {
                "step": 2,
                "agent": "question_generator",
                "action": "question_generation",
                "payload": payload
            }
        ]

        return self._build_plan("research_pipeline", steps)

    def _plan_learning(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan for building a learning module.
        """

        steps = [
            {
                "step": 1,
                "agent": "research_agent",
                "action": "concept_research",
                "payload": payload
            },
            {
                "step": 2,
                "agent": "learning_agent",
                "action": "learning_module_generation",
                "payload": payload
            },
            {
                "step": 3,
                "agent": "question_generator",
                "action": "question_generation",
                "payload": payload
            }
        ]

        return self._build_plan("learning_pipeline", steps)

    def _plan_idea_synthesis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan for generating new ideas across concepts.
        """

        steps = [
            {
                "step": 1,
                "agent": "idea_synthesizer",
                "action": "idea_generation",
                "payload": payload
            }
        ]

        return self._build_plan("idea_pipeline", steps)

    def _plan_curriculum(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan for generating a curriculum.
        """

        steps = [
            {
                "step": 1,
                "agent": "curriculum_builder",
                "action": "curriculum_generation",
                "payload": payload
            }
        ]

        return self._build_plan("curriculum_pipeline", steps)

    def _build_plan(self, plan_type: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Construct final plan structure.
        """

        return {
            "plan_type": plan_type,
            "created_at": datetime.utcnow().isoformat(),
            "steps": steps
        }