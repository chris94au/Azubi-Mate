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

class ResearchQueryDTO(BaseDTO):
    query: str
    category: Optional[str] = None
    include_external: bool = True
    limit: int = 5

class SourceEvaluationDTO(BaseDTO):
    source_name: str
    reliability_score: float
    notes: str

class ResearchResultDTO(BaseDTO):
    query: str
    summary: str
    local_results: List[KnowledgeItemDTO] = []
    external_sources: List[str] = []
    evaluations: List[SourceEvaluationDTO] = []
    found_locally: bool