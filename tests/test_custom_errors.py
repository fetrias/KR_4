from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_custom_exception_a():
    response = client.get("/errors/a")
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "CUSTOM_A"


def test_custom_exception_b():
    response = client.get("/errors/b/999")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "CUSTOM_B"


def test_validation_error():
    payload = {"name": "", "age": 10, "email": "not-an-email"}
    response = client.post("/users/validate", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "VALIDATION_ERROR"
    assert isinstance(body["details"], list)


def test_validation_success():
    payload = {"name": "Alex", "age": 20, "email": "alex@example.com"}
    response = client.post("/users/validate", json=payload)
    assert response.status_code == 200
    assert response.json() == payload
