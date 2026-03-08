from core.learning_loop import LearningLoop


class FakeAgent:

    def ingest_text(self, text):
        return {"concepts": []}

    def search_concepts(self, topic):
        return [{"name": "AI"}]

    def reason(self, topic):
        return "AI learns patterns"

    def reflect(self, topic):
        return "Improved reasoning"

    def close(self):
        pass


def test_learning_cycle():

    loop = LearningLoop()

    fake = FakeAgent()

    loop.memory_agent = fake
    loop.retrieval_agent = fake
    loop.reasoning_agent = fake
    loop.reflection_agent = fake

    result = loop.run_cycle("AI")

    assert "reasoning" in result