from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_research_concept():
    payload = {
        "concept": "Neural Networks",
        "domain": "AI",
        "query": "How do they work?"
    }

    response = client.post("/api/research/explore", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["concept"] == "Neural Networks"
    assert data["domain"] == "AI"


def test_list_research_results():
    response = client.get("/api/research/results")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_research_result():
    # First create a research result
    payload = {"concept": "Test Concept", "domain": "Test Domain"}
    create_response = client.post("/api/research/explore", json=payload)
    result_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/research/results/{result_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == result_id
    assert data["concept"] == "Test Concept"