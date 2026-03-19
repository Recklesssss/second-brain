import logging
import json
from typing import Dict, Any, List

from second_brain_ai.agents.base_agent import BaseAgent
from second_brain_ai.services.gemini_service import GeminiService
from second_brain_ai.backend.database.neo4j_service import db

logger = logging.getLogger(__name__)

class CurriculumBuilderAgent(BaseAgent):
    """
    Generates a sequenced learning curriculum for a domain using Gemini.
    """

    def __init__(self, agent_name: str = "curriculum_builder_agent"):
        super().__init__(agent_name)
        self.gemini = GeminiService()

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            domain = payload.get("domain", "General")
            user_id = payload.get("user_id", "user_1")

            # 1. Fetch user context (what they already know)
            # For now we'll assume a basic set of "known" nodes
            # In a real scenario, we'd query for nodes with mastery > threshold
            known_concepts = [] # Placeholder for user's existing knowledge

            # 2. Call Gemini to build the curriculum
            # We'll use the generate_research prompt as a base if a specific one isn't in the library
            # Or better, just build a custom prompt here for now
            prompt = (
                f"Act as a curriculum expert. Create a structured learning path for the domain: '{domain}'.\n"
                f"The user knows: {known_concepts}.\n"
                "Return a JSON object with:\n"
                "- title: A catchy name for the path\n"
                "- modules: list of {title, description, concepts_covered}\n"
                "- estimated_time: overall time like '10 hours'\n"
            )
            
            # Since there's no direct method in GeminiService for this yet, we'll use a generic one or add it later
            # For now, let's just use the generate_research method and adapt
            raw_result = await self.gemini._call(prompt)
            data = self.gemini._parse(raw_result, "curriculum")

            if "error" in data:
                return self.error_response("AGENT_FAILURE", data["error"])

            # 3. Persist the curriculum to Neo4j
            path_node = db.create_node(["LearningPath"], {
                "title": data.get("title", f"Curriculum for {domain}"),
                "domain": domain,
                "user_id": user_id,
                "progress": 0,
                "modules_count": len(data.get("modules", [])),
                "estimated_time": data.get("estimated_time", "Unknown")
            })

            # 4. Create module nodes and link them to the path
            for i, mod in enumerate(data.get("modules", [])):
                mod_node = db.create_node(["LearningModule"], {
                    "title": mod.get("title", "Untitled Module"),
                    "description": mod.get("description", ""),
                    "sequence": i,
                    "domain": domain
                })
                # Link: (Path)-[:HAS_MODULE]->(Module)
                db.create_relationship(path_node["id"], mod_node["id"], "HAS_MODULE")

            return self.success_response({
                "path_id": path_node["id"],
                "curriculum": data
            })

        except Exception as e:
            logger.exception("Curriculum builder failed")
            return self.error_response("AGENT_FAILURE", str(e))