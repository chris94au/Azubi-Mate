from fastapi import FastAPI
from azubi_mate_core.config import config

app = FastAPI(
    title=config.app_name,
    version=config.version,
    debug=config.debug
)

@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify backend status."""
    return {
        "status": "ok", 
        "app": config.app_name, 
        "version": config.version
    }