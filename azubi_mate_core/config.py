from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    """Core application configuration."""
    app_name: str = "Azubi-Mate API"
    debug: bool = False
    version: str = "0.1.0"
    
    model_config = SettingsConfigDict(env_prefix="AZUBI_")

config = AppConfig()