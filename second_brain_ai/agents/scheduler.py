import threading
import time
from typing import Dict, Any, Callable, List

from second_brain_ai.agents.workflow_orchestrator import AgentWorkflowOrchestrator


class AutonomousAgentScheduler:
    """
    Scheduler responsible for autonomous execution of agent workflows.

    Responsibilities:
    - maintain task queue
    - trigger workflows
    - run workflows in background threads
    - manage execution intervals
    """

    def __init__(self, orchestrator: AgentWorkflowOrchestrator):
        self.orchestrator = orchestrator
        self.task_queue: List[Dict[str, Any]] = []
        self.running = False
        self.thread = None
        self.interval = 5  # seconds

    def add_task(self, task_type: str, payload: Dict[str, Any]):
        """
        Add workflow task to scheduler queue.
        """

        self.task_queue.append(
            {
                "task_type": task_type,
                "payload": payload
            }
        )

    def start(self):
        """
        Start scheduler loop.
        """

        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stop scheduler loop.
        """

        self.running = False

    def _run_loop(self):
        """
        Background execution loop.
        """

        while self.running:

            if self.task_queue:

                task = self.task_queue.pop(0)

                try:
                    self.orchestrator.execute_workflow(
                        task["task_type"],
                        task["payload"]
                    )
                except Exception as e:
                    print(f"Scheduler task failed: {str(e)}")

            time.sleep(self.interval)