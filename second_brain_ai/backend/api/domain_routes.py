from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any
import uuid

router = APIRouter(prefix="/domains", tags=["domains"])

# Temporary in-memory store until graph service integration
DOMAINS: List[Dict[str, Any]] = []


@router.post("/")
async def create_domain(domain: Dict[str, Any]):

    domain_id = str(uuid.uuid4())

    new_domain = {
        "id": domain_id,
        "name": domain.get("name"),
        "created_at": datetime.utcnow().isoformat()
    }

    DOMAINS.append(new_domain)

    return {
        "status": "success",
        "data": new_domain,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/")
async def list_domains():
    return {
        "status": "success",
        "data": DOMAINS,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/{domain_id}")
async def get_domain(domain_id: str):
    for domain in DOMAINS:
        if domain["id"] == domain_id:
            return {
                "status": "success",
                "data": domain,
                "timestamp": datetime.utcnow().isoformat()
            }

    raise HTTPException(status_code=404, detail="Domain not found")
@router.get("/paths")
async def get_learning_paths():
    return {
        "status": "success",
        "data": [],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/curriculum")
async def generate_curriculum(payload: Dict[str, Any]):
    return {
        "status": "success",
        "data": {"message": "Curriculum generation placeholder"},
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/progress")
async def get_user_progress():
    return {
        "status": "success",
        "data": {},
        "timestamp": datetime.utcnow().isoformat()
    }
@router.get("/graph-summary")
async def graph_summary():

    nodes = []
    links = []

    # Domains → nodes
    for d in DOMAINS:
        nodes.append({
            "id": d["id"],
            "name": d["name"],
            "group": "Domain"
        })

    # Research results → concept nodes
    for r in DOMAINS:

        concept_id = f"concept_{r['concept']}"

        nodes.append({
            "id": concept_id,
            "name": r["concept"],
            "group": "Concept"
        })

        # link concept → domain
        links.append({
            "source": concept_id,
            "target": r["domain"]
        })

    return {
        "status": "success",
        "data": {
            "nodes": nodes,
            "links": links
        },
        "timestamp": datetime.utcnow().isoformat()
    }