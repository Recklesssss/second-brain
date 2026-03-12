from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_domain():
    payload = {
        "id": "ai",
        "name": "Artificial Intelligence"
    }

    response = client.post("/domains/", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_list_domains():
    response = client.get("/domains/")

    assert response.status_code == 200
    assert response.json()["status"] == "success"