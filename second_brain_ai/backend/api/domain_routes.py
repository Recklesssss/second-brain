from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import uuid

from second_brain_ai.backend.database.neo4j_service import db
router = APIRouter(prefix="/domains", tags=["domains"])

# Pydantic models for input validation
class DomainCreate(BaseModel):
    name: str
    description: Optional[str] = None

class DomainResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: str

@router.post("/")
async def create_domain(domain: DomainCreate):
    new_domain = db.create_node(["Domain"], {
        "name": domain.name,
        "description": domain.description
    })
    return {
        "status": "success",
        "data": new_domain,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/")
async def list_domains():
    domains = db.get_nodes_by_label("Domain")
    return {
        "status": "success",
        "data": domains,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/{domain_id}")
async def get_domain(domain_id: str):
    domain = db.get_node(domain_id)
    if domain and "Domain" in db.nodes.get(domain_id, {}).get("labels", []):
        return {
            "status": "success",
            "data": domain,
            "timestamp": datetime.utcnow().isoformat()
        }
    raise HTTPException(status_code=404, detail="Domain not found")

# Resource routes
class ResourceCreate(BaseModel):
    title: str
    content: str
    type: Optional[str] = "text"

class ResourceResponse(BaseModel):
    id: str
    title: str
    content: str
    type: str
    created_at: str

@router.post("/resources")
async def create_resource(resource: ResourceCreate):
    new_resource = db.create_node(["Resource"], {
        "title": resource.title,
        "content": resource.content,
        "type": resource.type
    })
    return {
        "status": "success",
        "data": new_resource,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/resources")
async def list_resources():
    resources = db.get_nodes_by_label("Resource")
    return {
        "status": "success",
        "data": resources,
        "timestamp": datetime.utcnow().isoformat()
    }