from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_domain():
    payload = {
        "name": "Artificial Intelligence",
        "description": "Study of intelligent systems"
    }

    response = client.post("/api/domains/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Artificial Intelligence"
    assert data["description"] == "Study of intelligent systems"


def test_list_domains():
    response = client.get("/api/domains/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_domain():
    # First create a domain
    payload = {"name": "Test Domain"}
    create_response = client.post("/api/domains/", json=payload)
    domain_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/domains/{domain_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == domain_id
    assert data["name"] == "Test Domain"