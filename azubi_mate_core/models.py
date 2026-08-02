# azubi_mate_core/models.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CoreModel(BaseModel):
    """Base model for all internal domain models."""
    model_config = ConfigDict(from_attributes=True)

class KnowledgeItemModel(CoreModel):
    id: str
    title: str
    category: str  # "Ausbildungsordnung", "Lerninhalt", "Fachwissen", "Gesetz", "Glossar"
    content: str
    tags: List[str] = []