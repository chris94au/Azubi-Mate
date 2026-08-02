from pydantic import BaseModel, ConfigDict

class CoreModel(BaseModel):
    """Base model for all internal domain models."""
    model_config = ConfigDict(from_attributes=True)