from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_research_concept():

    payload = {
        "concept": "Neural Networks",
        "domain": "AI"
    }

    response = client.post("/research/concept", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["data"]["concept"] == "Neural Networks"


def test_list_research_results():

    response = client.get("/research/results")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"