import time

from agents.scheduler import AutonomousAgentScheduler


class DummyOrchestrator:

    def __init__(self):
        self.executed = []

    def execute_workflow(self, task_type, payload):
        self.executed.append((task_type, payload))
        return {"status": "ok"}


def test_scheduler_executes_task():

    orchestrator = DummyOrchestrator()
    scheduler = AutonomousAgentScheduler(orchestrator)

    scheduler.add_task("research_concept", {"concept": "AI"})

    scheduler.start()

    time.sleep(6)

    scheduler.stop()

    assert len(orchestrator.executed) >= 1


def test_scheduler_queue():

    orchestrator = DummyOrchestrator()
    scheduler = AutonomousAgentScheduler(orchestrator)

    scheduler.add_task("idea_generation", {"concepts": ["AI", "Graph"]})

    assert len(scheduler.task_queue) == 1