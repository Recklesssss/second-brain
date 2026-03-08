from fastapi import FastAPI
from pydantic import BaseModel

from core.agent_orchestrator import AgentOrchestrator
from core.task_scheduler import TaskScheduler


app = FastAPI(title="AI Second Brain API")

orchestrator = AgentOrchestrator()
scheduler = TaskScheduler()


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class IngestRequest(BaseModel):
    text: str


class QueryRequest(BaseModel):
    topic: str


# --------------------------------------------------
# API Endpoints
# --------------------------------------------------

@app.get("/")
def root():

    return {"status": "AI Second Brain running"}


@app.post("/ingest")
def ingest_knowledge(req: IngestRequest):

    result = orchestrator.ingest_knowledge(req.text)

    return {"status": "ingested", "result": result}


@app.post("/query")
def query_knowledge(req: QueryRequest):

    result = orchestrator.query_knowledge(req.topic)

    return {"result": result}


@app.post("/reason")
def reason(req: QueryRequest):

    result = orchestrator.reason_about(req.topic)

    return {"result": result}


@app.post("/reflect")
def reflect(req: QueryRequest):

    result = orchestrator.reflect_on(req.topic)

    return {"result": result}


@app.post("/cycle")
def run_cycle(req: QueryRequest):

    result = orchestrator.run_autonomous_cycle(req.topic)

    return result


@app.post("/scheduler/start")
def start_scheduler(req: QueryRequest):

    scheduler.start(req.topic)

    return {"status": "scheduler started"}


@app.post("/scheduler/stop")
def stop_scheduler():

    scheduler.stop()

    return {"status": "scheduler stopped"}