from typing import Dict, Any, List

from agents.agent_executor import AgentExecutionManager
from agents.planning_engine import PlanningEngine


class AgentWorkflowOrchestrator:
    """
    The Workflow Orchestrator coordinates planning and execution.

    Responsibilities:

    1. Receive high-level requests
    2. Ask PlanningEngine for an execution plan
    3. Execute plan steps through AgentExecutionManager
    4. Aggregate results
    """

    def __init__(
        self,
        planning_engine: PlanningEngine,
        executor: AgentExecutionManager,
    ):
        self.planning_engine = planning_engine
        self.executor = executor

    def execute_workflow(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a full agent workflow.

        Steps:
        - generate plan
        - execute steps sequentially
        - collect results
        """

        plan = self.planning_engine.plan(task_type, payload)

        results: List[Dict[str, Any]] = []

        for step in plan["steps"]:
            agent_name = step["agent"]
            action = step["action"]
            step_payload = step["payload"]

            result = self.executor.execute(agent_name, action, step_payload)

            results.append(
                {
                    "agent": agent_name,
                    "action": action,
                    "result": result,
                }
            )

        return {
            "plan_type": plan["plan_type"],
            "steps_executed": len(results),
            "results": results,
        }