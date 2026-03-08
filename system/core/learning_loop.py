from agents.memory_ingestion_agent import MemoryIngestionAgent
from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent
from agents.reasoning_agent import ReasoningAgent
from agents.reflection_agent import ReflectionAgent


class LearningLoop:
    """
    Central controller that runs the AI Second Brain cognition cycle.
    """

    def __init__(self):

        self.memory_agent = MemoryIngestionAgent()
        self.retrieval_agent = KnowledgeRetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.reflection_agent = ReflectionAgent()

    # --------------------------------------------------
    # Learning Cycle
    # --------------------------------------------------

    def ingest(self, text: str):

        return self.memory_agent.ingest_text(text)

    def retrieve(self, topic: str):

        return self.retrieval_agent.search_concepts(topic)

    def reason(self, topic: str):

        return self.reasoning_agent.reason(topic)

    def reflect(self, topic: str):

        return self.reflection_agent.reflect(topic)

    # --------------------------------------------------
    # Full Cognitive Cycle
    # --------------------------------------------------

    def run_cycle(self, topic: str):

        knowledge = self.retrieve(topic)

        reasoning = self.reason(topic)

        reflection = self.reflect(topic)

        return {
            "retrieved_knowledge": knowledge,
            "reasoning": reasoning,
            "reflection": reflection
        }

    # --------------------------------------------------

    def close(self):

        self.memory_agent.close()
        self.retrieval_agent.close()
        self.reasoning_agent.close()
        self.reflection_agent.close()