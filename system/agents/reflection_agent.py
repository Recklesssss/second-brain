from ai.gemini_service import GeminiService
from agents.reasoning_agent import ReasoningAgent


class ReflectionAgent:
    """
    Evaluates reasoning outputs and improves them.
    """

    def __init__(self):

        self.llm = GeminiService()
        self.reasoner = ReasoningAgent()

    # --------------------------------------------------
    # Reflection
    # --------------------------------------------------

    def reflect(self, topic: str):

        reasoning_output = self.reasoner.reason(topic)

        prompt = f"""
You are an AI self-reflection system.

Evaluate the reasoning below.

REASONING:
{reasoning_output}

Perform the following:

1. Identify weaknesses or missing logic
2. Improve the reasoning
3. Provide a refined explanation
"""

        return self.llm.generate(prompt)

    # --------------------------------------------------

    def close(self):

        self.reasoner.close()