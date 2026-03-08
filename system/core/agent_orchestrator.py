from core.learning_loop import LearningLoop


class AgentOrchestrator:
    """
    Coordinates execution of AI agents and manages the learning loop.
    """

    def __init__(self):

        self.learning_loop = LearningLoop()

    # --------------------------------------------------
    # Agent Execution
    # --------------------------------------------------

    def ingest_knowledge(self, text: str):

        return self.learning_loop.ingest(text)

    def query_knowledge(self, topic: str):

        return self.learning_loop.retrieve(topic)

    def reason_about(self, topic: str):

        return self.learning_loop.reason(topic)

    def reflect_on(self, topic: str):

        return self.learning_loop.reflect(topic)

    # --------------------------------------------------
    # Autonomous Cycle
    # --------------------------------------------------

    def run_autonomous_cycle(self, topic: str):

        result = self.learning_loop.run_cycle(topic)

        return {
            "status": "completed",
            "topic": topic,
            "result": result
        }

    # --------------------------------------------------

    def shutdown(self):

        self.learning_loop.close()