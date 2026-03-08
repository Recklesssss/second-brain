from core.task_scheduler import TaskScheduler


class FakeOrchestrator:

    def run_autonomous_cycle(self, topic):

        return {"status": "completed"}

    def shutdown(self):
        pass


def test_scheduler_start_stop():

    scheduler = TaskScheduler(interval_seconds=1)

    scheduler.orchestrator = FakeOrchestrator()

    scheduler.start("AI")

    assert scheduler.running is True

    scheduler.stop()

    assert scheduler.running is False