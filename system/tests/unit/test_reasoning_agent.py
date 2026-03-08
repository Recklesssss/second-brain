from agents.reasoning_agent import ReasoningAgent


class FakeLLM:

    def generate(self, prompt):

        return "Key insight: AI evolves through machine learning."


class FakeRetriever:

    def search_concepts(self, topic):

        return [
            {"name": "AI", "description": "Artificial Intelligence"},
            {"name": "Machine Learning", "description": "Learning algorithms"}
        ]

    def close(self):
        pass


def test_reasoning():

    agent = ReasoningAgent()

    agent.llm = FakeLLM()
    agent.retriever = FakeRetriever()

    result = agent.reason("AI")

    assert "insight" in result.lower()