# azubi_mate_core/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar
from .dto import (
    KnowledgeItemDTO,
    KnowledgeSearchQueryDTO,
    ResearchQueryDTO,
    ResearchResultDTO,
    LLMRequestDTO,
    LLMResponseDTO,
)

class BaseEngine(ABC):
    """Base interface for all engines in Azubi-Mate."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initializes the engine."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns the current status of the engine."""
        pass

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Base interface for repository pattern data access."""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Adds an entity to the persistence store."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Retrieves an entity by its unique identifier."""
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        """Retrieves all entities from the persistence store."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Deletes an entity by its unique identifier."""
        pass

class KnowledgeEngineInterface(BaseEngine, ABC):
    """Interface for the Knowledge Engine."""

    @abstractmethod
    def add_knowledge(self, item: KnowledgeItemDTO) -> KnowledgeItemDTO:
        """Adds or updates a knowledge item."""
        pass

    @abstractmethod
    def get_knowledge(self, item_id: str) -> Optional[KnowledgeItemDTO]:
        """Retrieves a knowledge item by ID."""
        pass

    @abstractmethod
    def search_knowledge(self, query: KnowledgeSearchQueryDTO) -> List[KnowledgeItemDTO]:
        """Searches knowledge items based on query and category."""
        pass

    @abstractmethod
    def list_knowledge(self) -> List[KnowledgeItemDTO]:
        """Lists all knowledge items."""
        pass

class ResearchEngineInterface(BaseEngine, ABC):
    """Interface for the Research Engine."""

    @abstractmethod
    def research(self, query: ResearchQueryDTO) -> ResearchResultDTO:
        """Conducts research across local knowledge base and external sources if needed."""
        pass

class LLMProvider(ABC):
    """Interface for LLM providers (Ollama, OpenAI, Gemini, etc.)."""

    @abstractmethod
    def generate(self, request: LLMRequestDTO) -> LLMResponseDTO:
        """Generates a response from the LLM provider."""
        pass