from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any, List

router = APIRouter(prefix="/learning", tags=["learning"])

# Temporary in-memory learning modules
LEARNING_MODULES: List[Dict[str, Any]] = []


@router.post("/module")
async def create_learning_module(module: Dict[str, Any]):

    module["created_at"] = datetime.utcnow().isoformat()

    LEARNING_MODULES.append(module)

    return {
        "status": "success",
        "data": module,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/modules")
async def list_learning_modules():

    return {
        "status": "success",
        "data": LEARNING_MODULES,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/modules/{module_id}")
async def get_learning_module(module_id: str):

    for module in LEARNING_MODULES:

        if module.get("id") == module_id:

            return {
                "status": "success",
                "data": module,
                "timestamp": datetime.utcnow().isoformat()
            }

    return {
        "status": "error",
        "error_code": "MODULE_NOT_FOUND",
        "message": "Learning module not found",
        "timestamp": datetime.utcnow().isoformat()
    }