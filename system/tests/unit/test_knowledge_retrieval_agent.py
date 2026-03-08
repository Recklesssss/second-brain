from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent


class FakeLLM:

    def generate(self, prompt):
        return "AI is the simulation of intelligence."


class FakeGraph:

    def query(self, q, params=None):

        return [
            {"name": "AI", "description": "Artificial Intelligence"},
            {"name": "Machine Learning", "description": "Subset of AI"}
        ]

    def close(self):
        pass


def test_answer_question():

    agent = KnowledgeRetrievalAgent()

    agent.llm = FakeLLM()
    agent.graph = FakeGraph()

    answer = agent.answer_question("What is AI?")

    assert "intelligence" in answer.lower()