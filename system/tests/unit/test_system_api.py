from fastapi.testclient import TestClient
from api.system_api import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_cycle_endpoint():

    response = client.post("/cycle", json={"topic": "AI"})

    assert response.status_code == 200