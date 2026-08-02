# tests/test_phase_2.py
from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core.config import config

client = TestClient(app)

def test_health_and_api_status() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response_api = client.get("/api/v1/status")
    assert response_api.status_code == 200
    assert response_api.json()["status"] == "active"

def test_error_responses() -> None:
    response_nf = client.get("/api/v1/test-not-found")
    assert response_nf.status_code == 404
    assert response_nf.json()["error"] == "Not Found"

    response_val = client.get("/api/v1/test-validation")
    assert response_val.status_code == 422
    assert response_val.json()["error"] == "Validation Error"

    response_err = client.get("/api/v1/test-core-error")
    assert response_err.status_code == 400
    assert response_err.json()["error"] == "Application Error"