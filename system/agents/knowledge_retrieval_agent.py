from ai.gemini_service import GeminiService
from core.knowledge_graph import KnowledgeGraph


class KnowledgeRetrievalAgent:
    """
    Agent responsible for retrieving relevant concepts from the knowledge graph
    and generating answers using the LLM.
    """

    def __init__(self):
        self.llm = GeminiService()
        self.graph = KnowledgeGraph()

    # --------------------------------------------------
    # Graph Search
    # --------------------------------------------------

    def search_concepts(self, keyword: str):

        query = """
        MATCH (c:Concept)
        WHERE toLower(c.name) CONTAINS toLower($keyword)
        RETURN c.name AS name, c.description AS description
        LIMIT 10
        """

        return self.graph.query(query, {"keyword": keyword})

    # --------------------------------------------------
    # Question Answering
    # --------------------------------------------------

    def answer_question(self, question: str):

        concepts = self.search_concepts(question)

        context = ""

        for c in concepts:
            context += f"{c['name']}: {c.get('description','')}\n"

        prompt = f"""
Use the knowledge context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}

Provide a clear answer.
"""

        return self.llm.generate(prompt)

    # --------------------------------------------------

    def close(self):
        self.graph.close()