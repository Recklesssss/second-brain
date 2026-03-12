from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any, List

router = APIRouter(prefix="/research", tags=["research"])

# Temporary in-memory research store
RESEARCH_RESULTS: List[Dict[str, Any]] = []


@router.post("/explore")
async def research_concept(payload: Dict[str, Any]):
    concept = payload.get("concept")
    domain = payload.get("domain")

    result = {
        "concept": concept,
        "domain": domain,
        "summary": f"Research summary for {concept}",
        "created_at": datetime.utcnow().isoformat()
    }

    RESEARCH_RESULTS.append(result)

    return {
        "status": "success",
        "data": result,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/results")
async def list_research_results():

    return {
        "status": "success",
        "data": RESEARCH_RESULTS,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/results/{concept}")
async def get_research_result(concept: str):

    for r in RESEARCH_RESULTS:
        if r.get("concept") == concept:
            return {
                "status": "success",
                "data": r,
                "timestamp": datetime.utcnow().isoformat()
            }

    return {
        "status": "error",
        "error_code": "RESEARCH_NOT_FOUND",
        "message": "Research result not found",
        "timestamp": datetime.utcnow().isoformat()
    }