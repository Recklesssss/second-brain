from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_learning_module():
    payload = {
        "title": "Intro to AI",
        "description": "Basic concepts of artificial intelligence",
        "domain_id": "ai"
    }

    response = client.post("/api/learning/module", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Intro to AI"
    assert data["description"] == "Basic concepts of artificial intelligence"


def test_list_learning_modules():
    response = client.get("/api/learning/modules")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_learning_module():
    # First create a module
    payload = {"title": "Test Module"}
    create_response = client.post("/api/learning/module", json=payload)
    module_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/learning/modules/{module_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == module_id
    assert data["title"] == "Test Module"