# backend/main.py
from fastapi import FastAPI
from azubi_mate_core.config import config, logger
from backend.exceptions import register_exception_handlers
from backend.api.router import api_router

app = FastAPI(
    title=config.app_name,
    version=config.version,
    debug=config.debug,
)

# Register global error handlers
register_exception_handlers(app)

# Include API routers
app.include_router(api_router)

@app.on_event("startup")
def startup_event() -> None:
    logger.info(f"Starting {config.app_name} v{config.version}...")

@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend status."""
    return {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version,
    }