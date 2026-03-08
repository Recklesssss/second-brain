from ai.gemini_service import GeminiService
from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent


class ReasoningAgent:
    """
    Performs higher level reasoning using knowledge retrieved
    from the knowledge graph.
    """

    def __init__(self):

        self.llm = GeminiService()
        self.retriever = KnowledgeRetrievalAgent()

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    def reason(self, topic: str):

        knowledge = self.retriever.search_concepts(topic)

        context = ""

        for k in knowledge:
            context += f"{k['name']}: {k.get('description','')}\n"

        prompt = f"""
You are an intelligent reasoning engine.

Using the knowledge below, infer deeper insights,
connections, and possible implications.

KNOWLEDGE:
{context}

TOPIC:
{topic}

Return structured reasoning including:
1. Key insight
2. Explanation
3. Possible implications
"""

        return self.llm.generate(prompt)

    # --------------------------------------------------

    def close(self):

        self.retriever.close()