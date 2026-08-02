# azubi_mate_core/config.py
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    """Core application configuration."""
    app_name: str = "Azubi-Mate API"
    debug: bool = False
    version: str = "0.1.0"
    log_level: str = "INFO"
    database_path: str = "azubi_mate.db"
    
    model_config = SettingsConfigDict(env_prefix="AZUBI_")

config = AppConfig()

def setup_logging() -> logging.Logger:
    """Configures and returns the root logger for Azubi-Mate."""
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger("azubi_mate")

logger = setup_logging()