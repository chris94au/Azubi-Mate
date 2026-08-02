# azubi_mate_core/dto.py
from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    """Base Data Transfer Object for all module communications."""
    model_config = ConfigDict(from_attributes=True)