from fastapi.testclient import TestClient
from backend.main import app
from azubi_mate_core.config import config
from azubi_mate_core.exceptions import AzubiMateException

client = TestClient(app)

def test_backend_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version
    }

def test_core_imports_and_usage() -> None:
    exc = AzubiMateException("Test Error")
    assert exc.message == "Test Error"
    assert config.version == "0.1.0"