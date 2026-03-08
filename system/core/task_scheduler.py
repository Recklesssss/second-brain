import threading
import time

from core.agent_orchestrator import AgentOrchestrator


class TaskScheduler:
    """
    Runs AI tasks automatically at scheduled intervals.
    """

    def __init__(self, interval_seconds: int = 60):

        self.interval = interval_seconds
        self.orchestrator = AgentOrchestrator()
        self.running = False
        self.thread = None

    # --------------------------------------------------
    # Scheduler Loop
    # --------------------------------------------------

    def _loop(self, topic: str):

        while self.running:

            try:
                result = self.orchestrator.run_autonomous_cycle(topic)

                print("Cycle completed:", result)

            except Exception as e:

                print("Scheduler error:", e)

            time.sleep(self.interval)

    # --------------------------------------------------

    def start(self, topic: str):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            args=(topic,),
            daemon=True
        )

        self.thread.start()

    # --------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        self.orchestrator.shutdown()