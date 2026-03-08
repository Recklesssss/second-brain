from ai.gemini_service import GeminiService
from core.knowledge_graph import KnowledgeGraph
import json
import uuid


class MemoryIngestionAgent:
    """
    Agent responsible for converting raw text into structured knowledge
    and storing it in the Neo4j knowledge graph.
    """

    def __init__(self):

        self.llm = GeminiService()
        self.graph = KnowledgeGraph()

    def ingest_text(self, text: str):

        prompt = f"""
Extract structured knowledge from the following text.

Return JSON in this format:

{{
    "concepts": [
        {{
            "name": "",
            "description": ""
        }}
    ],
    "relationships": [
        {{
            "source": "",
            "target": "",
            "type": "RELATED_TO"
        }}
    ]
}}

TEXT:
{text}
"""

        response = self.llm.generate_json(prompt)

        try:
            data = json.loads(response)
        except Exception:
            raise ValueError("LLM returned invalid JSON")

        self._store_concepts(data)

        return data

    # ----------------------------------------

    def _store_concepts(self, data):

        concept_ids = {}

        for concept in data.get("concepts", []):

            node_id = str(uuid.uuid4())

            self.graph.create_node(
                "Concept",
                {
                    "id": node_id,
                    "name": concept["name"],
                    "description": concept.get("description", "")
                }
            )

            concept_ids[concept["name"]] = node_id

        for rel in data.get("relationships", []):

            src = concept_ids.get(rel["source"])
            tgt = concept_ids.get(rel["target"])

            if not src or not tgt:
                continue

            self.graph.create_relationship(
                "Concept",
                src,
                rel["type"],
                "Concept",
                tgt
            )

    def close(self):

        self.graph.close()