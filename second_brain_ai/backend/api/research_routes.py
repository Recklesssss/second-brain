import sys
import os
from pathlib import Path

# Calculate the path to the 'second_brain_ai' root directory
# (Going up two levels from 'backend/api/research_routes.py')
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    pass # Managed perfectly by root execution now

# Now this import will work



from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid

from second_brain_ai.agents import get_agent_executor

router = APIRouter(prefix="/research", tags=["research"])

# Pydantic models
class ResearchRequest(BaseModel):
    concept: str
    domain: Optional[str] = None
    query: Optional[str] = None

class ResearchResult(BaseModel):
    id: str
    concept: str
    domain: Optional[str] = None
    query: Optional[str] = None
    summary: str
    created_at: str

from second_brain_ai.backend.database.neo4j_service import db

executor = get_agent_executor()


@router.post("/explore")
async def research_concept(request: ResearchRequest):
    payload = request.dict()

    # Execute through agent pipeline to use Gemini integration
    response = await executor.execute_agent("research_agent", payload)

    if response.get("status") == "success":
        data = response.get("data", {})
        data["concept"] = request.concept
        data["query"] = request.query
        data["domain"] = request.domain
        db.create_node(["ResearchResult"], data)
        return response

    raise HTTPException(status_code=500, detail=response.get("message", "Research failed"))


@router.get("/results")
async def list_research_results():
    results = db.get_nodes_by_label("ResearchResult")
    return {
        "status": "success",
        "data": results,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/results/{result_id}")
async def get_research_result(result_id: str):
    result = db.get_node(result_id)
    if result and "ResearchResult" in db.nodes.get(result_id, {}).get("labels", []):
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    raise HTTPException(status_code=404, detail="Research result not found")


@router.get("/graph-summary")
async def graph_summary():
    nodes = []
    links = []

    for node_id, node_data in db.nodes.items():
        if "User" in node_data["labels"]:
            continue
            
        nodes.append({
            "id": node_id,
            "name": node_data["properties"].get("name", node_data["properties"].get("title", node_id)),
            "group": node_data["labels"][0]
        })

    for edge in db.edges:
        links.append({
            "source": edge["source"],
            "target": edge["target"],
            "label": edge["type"]
        })

    return {
        "status": "success",
        "data": {
            "nodes": nodes,
            "links": links
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/insights")
async def get_insights():
    """
    Runs the ThinkingEngineAgent to derive patterns, gaps, and insights
    from the current knowledge graph state.
    """
    response = await executor.execute_agent("thinking_engine_agent", {})
    if response.get("status") == "success":
        data = response.get("data", {})
        # Flatten insights list for frontend rendering
        insights = data.get("insights", [])
        patterns = data.get("patterns", [])
        gaps = data.get("knowledge_gaps", [])
        combined = (
            [{"id": f"insight-{i}", "type": "synthesis", "title": x.get("content", ""),
              "description": x.get("content", ""), "concepts": [], "confidence": 0.8} for i, x in enumerate(insights)]
            + [{"id": f"pattern-{i}", "type": "pattern", "title": x.get("description", ""),
                "description": x.get("description", ""), "concepts": [], "confidence": 0.75} for i, x in enumerate(patterns)]
            + [{"id": f"gap-{i}", "type": "gap", "title": f"Knowledge Gap: {x.get('area', '')}",
                "description": f"Severity: {x.get('severity', 'unknown')}", "concepts": [], "confidence": 0.9} for i, x in enumerate(gaps)]
        )
        return {
            "status": "success",
            "data": combined,
            "timestamp": datetime.utcnow().isoformat()
        }
    return {
        "status": "success",
        "data": [],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/synthesize")
async def synthesize_ideas(payload: Dict[str, Any]):
    """
    Calls the IdeaSynthesizerAgent (Gemini) to combine a list of concepts
    into a novel synthesized idea with applications.
    """
    concept_ids: list = payload.get("concept_ids", [])
    # Resolve concept IDs to names for better prompt context
    concepts = []
    for cid in concept_ids:
        node = db.get_node(cid)
        if node:
            concepts.append({"name": node.get("name", cid), "id": cid})
        else:
            concepts.append({"name": cid, "id": cid})

    if not concepts:
        raise HTTPException(status_code=400, detail="concept_ids required")

    response = await executor.execute_agent("idea_synthesizer_agent", {"concepts": concepts})
    if response.get("status") == "success":
        data = response.get("data", {})
        # Persist synthesized idea node
        db.create_node(["Idea"], {
            "name": data.get("idea_title", "Synthesized Idea"),
            "description": data.get("description", ""),
            "applications": str(data.get("potential_applications", [])),
            "source": "gemini"
        })
        return response
    raise HTTPException(status_code=500, detail=response.get("message", "Synthesis failed"))
