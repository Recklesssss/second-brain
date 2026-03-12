from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_learning_module():

    payload = {
        "id": "module_1",
        "title": "Intro to AI"
    }

    response = client.post("/learning/module", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_list_modules():

    response = client.get("/learning/modules")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"