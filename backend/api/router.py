# backend/api/router.py
from fastapi import APIRouter
from azubi_mate_core import config, NotFoundError, ValidationException, AzubiMateException

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/status")
def api_status() -> dict[str, str]:
    """API status endpoint."""
    return {
        "status": "active",
        "app": config.app_name,
        "version": config.version,
    }

@api_router.get("/test-not-found")
def trigger_not_found() -> None:
    raise NotFoundError("Resource not found")

@api_router.get("/test-validation")
def trigger_validation() -> None:
    raise ValidationException("Invalid input data")

@api_router.get("/test-core-error")
def trigger_core_error() -> None:
    raise AzubiMateException("Core general error")