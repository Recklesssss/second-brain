from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from api.domain_routes import router as domain_router
from api.learning_routes import router as learning_router
from api.research_routes import router as research_router

app = FastAPI(
    title="AI Second Brain API",
    description="Backend API for the AI Second Brain Platform",
    version="1.0.0",
)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTANT: add /api prefix
app.include_router(domain_router, prefix="/api")
app.include_router(learning_router, prefix="/api")
app.include_router(research_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "status": "success",
        "data": {"message": "AI Second Brain API running"},
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    return {
        "status": "success",
        "data": {
            "service": "ai_second_brain",
            "status": "healthy"
        },
        "timestamp": datetime.utcnow().isoformat()
    }