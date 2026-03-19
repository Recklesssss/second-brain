from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/learning", tags=["learning"])

# Pydantic models
class LearningModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    domain_id: Optional[str] = None

class LearningModuleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    domain_id: Optional[str] = None
    created_at: str

class LearningModuleGenerateRequest(BaseModel):
    concept: str
    domain: str
    user_id: Optional[str] = "user_1"

class QuestionRequest(BaseModel):
    concept: str
    domain: Optional[str] = None
    user_id: Optional[str] = "user_1"

class PathProgressRequest(BaseModel):
    completed_modules: int

class CurriculumRequest(BaseModel):
    domain: str
    user_id: Optional[str] = "user_1"

from second_brain_ai.backend.database.neo4j_service import db
from second_brain_ai.agents import get_agent_executor

executor = get_agent_executor()


@router.post("/module")
async def create_learning_module(module: LearningModuleCreate):
    new_module = db.create_node(["LearningModule"], {
        "title": module.title,
        "description": module.description,
        "domain_id": module.domain_id
    })
    return {
        "status": "success",
        "data": new_module,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/modules")
async def list_learning_modules():
    modules = db.get_nodes_by_label("LearningModule")
    return {
        "status": "success",
        "data": modules,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/modules/{module_id}")
async def get_learning_module(module_id: str):
    module = db.get_node(module_id)
    if module and "LearningModule" in db.nodes.get(module_id, {}).get("labels", []):
        return {
            "status": "success",
            "data": module,
            "timestamp": datetime.utcnow().isoformat()
        }
    raise HTTPException(status_code=404, detail="Learning module not found")


@router.get("/paths")
async def get_learning_paths():
    paths = db.get_learning_path(user_id="user_1")
    return {
        "status": "success",
        "data": paths,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/paths/{path_id}/modules")
async def get_path_modules(path_id: str):
    modules = db.get_modules_for_path(path_id)
    return {
        "status": "success",
        "data": modules,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/generate")
async def generate_learning_module_ai(request: LearningModuleGenerateRequest):
    """
    Calls the LearningAgent (Gemini) to generate a tailored learning module
    for a specific concept, adapted to the user's known concepts.
    """
    payload = {
        "concept_data": {"name": request.concept, "domain": request.domain},
        "user_id": request.user_id,
    }
    response = await executor.execute_agent("learning_agent", payload)
    if response.get("status") == "success":
        data = response.get("data", {})
        # Persist the generated module
        db.create_node(["LearningModule"], {
            "title": data.get("title", f"Module: {request.concept}"),
            "description": data.get("content", ""),
            "domain_id": request.domain,
            "difficulty": data.get("difficulty", ""),
            "source": "gemini"
        })
        return response
    raise HTTPException(status_code=500, detail=response.get("message", "Learning generation failed"))


@router.post("/questions")
async def generate_questions(request: QuestionRequest):
    """
    Calls the QuestionGenerator agent (Gemini) to produce a quiz question
    for the given concept, adapted to the user's mastery level.
    """
    payload = {
        "concept_data": {"name": request.concept, "domain": request.domain},
        "user_id": request.user_id,
    }
    response = await executor.execute_agent("question_generator", payload)
    if response.get("status") == "success":
        return response
    raise HTTPException(status_code=500, detail=response.get("message", "Question generation failed"))


@router.post("/curriculum")
async def generate_curriculum(request: CurriculumRequest):
    """
    Calls the CurriculumBuilderAgent to produce a sequenced learning
    path for a given domain, based on existing knowledge graph data.
    """
    payload = {
        "domain": request.domain,
        "user_id": request.user_id,
    }
    response = await executor.execute_agent("curriculum_builder_agent", payload)
    if response.get("status") == "success":
        return response
    raise HTTPException(status_code=500, detail=response.get("message", "Curriculum generation failed"))


@router.post("/paths/{path_id}/progress")
async def update_path_progress(path_id: str, request: PathProgressRequest):
    path = db.get_node(path_id)
    if not path or "LearningPath" not in db.nodes.get(path_id, {}).get("labels", []):
        raise HTTPException(status_code=404, detail="Path not found")
        
    modules_count = path.get("modules_count", 1)
    path["completedModules"] = request.completed_modules
    path["progress"] = min(100, int((request.completed_modules / max(1, modules_count)) * 100))
    
    return {
        "status": "success",
        "data": path,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/progress")
async def get_user_progress():
    return {
        "status": "success",
        "data": {},
        "timestamp": datetime.utcnow().isoformat()
    }
