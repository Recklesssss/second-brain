from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid

from second_brain_ai.backend.database.neo4j_service import db
router = APIRouter(prefix="/concepts", tags=["concepts"])

# Pydantic models for input validation
class ConceptResponse(BaseModel):
    id: str
    name: str
    domain_id: Optional[str] = None
    created_at: str

class RelationshipResponse(BaseModel):
    source: str
    target: str
    type: str

# Removed temporary in-memory store

@router.get("/")
async def list_concepts(domain: Optional[str] = None):
    concepts = db.get_nodes_by_label("Concept")
    if domain:
        # filter by BELONGS_TO edge
        valid_ids = {e["source"] for e in db.edges if e["type"] == "BELONGS_TO" and e["target"] == domain}
        concepts = [c for c in concepts if c["id"] in valid_ids]
    
    return {
        "status": "success",
        "data": concepts,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/{concept_id}/relationships")
async def get_concept_relationships(concept_id: str):
    rels = []
    for e in db.edges:
        if e["source"] == concept_id or e["target"] == concept_id:
            rels.append({"source": e["source"], "target": e["target"], "type": e["type"]})
    
    return {
        "status": "success",
        "data": rels,
        "timestamp": datetime.utcnow().isoformat()
    }

