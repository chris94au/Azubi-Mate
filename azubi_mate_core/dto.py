# azubi_mate_core/dto.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class BaseDTO(BaseModel):
    """Base Data Transfer Object for all module communications."""
    model_config = ConfigDict(from_attributes=True)

class KnowledgeItemDTO(BaseDTO):
    id: str
    title: str
    category: str
    content: str
    tags: List[str] = []

class KnowledgeSearchQueryDTO(BaseDTO):
    query: str
    category: Optional[str] = None
    limit: int = 10