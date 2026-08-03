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

class LLMRequestDTO(BaseDTO):
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None

class LLMResponseDTO(BaseDTO):
    text: str
    model: str
    provider: str
    usage: Optional[dict] = None

class ReportRequestDTO(BaseDTO):
    report_type: str  # "tagesbericht", "wochenbericht", "monatsbericht"
    bullet_points: List[str]
    trainee_name: Optional[str] = None
    department: Optional[str] = None
    date: Optional[str] = None
    week_number: Optional[int] = None
    month: Optional[str] = None
    year: Optional[int] = None

class ReportDTO(BaseDTO):
    id: str
    report_type: str
    title: str
    activities: List[str] = []
    learning_content: List[str] = []
    technical_terms: List[str] = []
    summary: str
    date: Optional[str] = None
    week_number: Optional[int] = None
    month: Optional[str] = None
    year: Optional[int] = None
    status: str = "draft"  # "draft", "confirmed"

class DocumentExportRequestDTO(BaseDTO):
    content: str
    title: str
    format: str = "pdf"  # "pdf", "docx", "txt"
    metadata: dict = {}

class DocumentExportResultDTO(BaseDTO):
    file_path: Optional[str] = None
    format: str
    success: bool
    message: str