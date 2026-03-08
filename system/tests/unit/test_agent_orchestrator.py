from core.agent_orchestrator import AgentOrchestrator


class FakeLoop:

    def ingest(self, text):
        return {"status": "ingested"}

    def retrieve(self, topic):
        return [{"name": "AI"}]

    def reason(self, topic):
        return "AI learns patterns"

    def reflect(self, topic):
        return "Improved reasoning"

    def run_cycle(self, topic):
        return {"reasoning": "AI", "reflection": "better AI"}

    def close(self):
        pass


def test_orchestrator_cycle():

    orchestrator = AgentOrchestrator()

    orchestrator.learning_loop = FakeLoop()

    result = orchestrator.run_autonomous_cycle("AI")

    assert result["status"] == "completed"