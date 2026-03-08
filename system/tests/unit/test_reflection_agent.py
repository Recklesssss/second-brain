from agents.reflection_agent import ReflectionAgent


class FakeLLM:

    def generate(self, prompt):

        return "Improved reasoning about AI."


class FakeReasoner:

    def reason(self, topic):

        return "AI learns from data."


    def close(self):
        pass


def test_reflection():

    agent = ReflectionAgent()

    agent.llm = FakeLLM()
    agent.reasoner = FakeReasoner()

    result = agent.reflect("AI")

    assert "improved" in result.lower()